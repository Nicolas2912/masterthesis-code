import fitz
import numpy as np
from pathlib import Path
import pymupdf4llm
from typing import List, Dict, Optional, Union
import shutil
import os
from tqdm import tqdm
import re
import imagehash
from PIL import Image
import pandas as pd


def extract_all_figures(
        pdf_path: str,
        output_dir: str,
        pages: Optional[List[int]] = None,
        black_threshold: float = 0.3,
        white_threshold: float = 0.6,
        y0_threshold: float = 105,
        min_cluster_size: float = 100,
        dpi: int = 200,
        graphics_limit: int = 100
):
    """
    Extract figures using three methods:
    1. Vector graphics using extract_clustered_figures
    2. Embedded images using page.get_images()
    3. Images through pymupdf4llm.to_markdown

    Ensures correct sequential figure numbering per page.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Open document once to get total pages
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    doc.close()

    if not pages:
        pages = list(range(1, total_pages + 1))  # 1-based page numbers

    # First pass: extract vector graphics and embedded images
    for page_num in tqdm(pages, desc="Processing vector graphics and embedded images"):
        # Track figure numbers for this page
        figures_on_page = set()

        # Extract vector graphics
        vector_results = extract_clustered_figures(
            pdf_path=pdf_path,
            page_number=page_num,
            output_dir=str(output_dir)
        )

        # Get the current figure numbers on this page from vector graphics
        for file in output_dir.glob(f"page_{page_num}_figure_*.png"):
            try:
                figure_num = int(re.search(r'figure_(\d+)', file.name).group(1))
                figures_on_page.add(figure_num)
            except (AttributeError, ValueError):
                continue

        # Calculate next available figure number for this page
        next_figure_num = max(figures_on_page, default=0) + 1

        # Extract embedded images
        doc = fitz.open(pdf_path)
        page = doc[page_num - 1]
        image_list = page.get_images()

        skipped_images = 0

        # Extract each embedded image with correct numbering
        for img in image_list:
            try:
                # Get image dimensions from tuple
                # img tuple format: (xref, smask, width, height, bpc, colorspace, ...)
                width = img[2]
                height = img[3]

                # Skip small images
                if width < 50 or height < 50:
                    skipped_images += 1
                    continue

                xref = img[0]
                base_image = doc.extract_image(xref)

                if base_image:
                    # Check if image contains meaningful content
                    if not is_content_image(base_image["image"]):
                        skipped_images += 1
                        continue

                    # Use next available figure number
                    output_path = output_dir / f"page_{page_num}_figure_{next_figure_num}.png"

                    # Save image
                    with open(output_path, "wb") as f:
                        f.write(base_image["image"])

                    next_figure_num += 1

            except Exception as e:
                print(f"Error extracting image on page {page_num}: {str(e)}")
                continue

        doc.close()

        # print(f"Page {page_num}: Processed {next_figure_num - 1} total figures")

    # Second pass: Use to_markdown to catch any remaining images
    # Convert to 0-based page numbers for to_markdown
    pages_0_indexed = [page - 1 for page in pages]

    print("\nRunning to_markdown extraction...")
    md_text = pymupdf4llm.to_markdown(
        doc=pdf_path,
        pages=pages_0_indexed,
        page_chunks=True,
        write_images=True,
        image_path=str(output_dir),
        image_format="png",
        dpi=dpi
    )

    # The to_markdown function will save images as "{PDF_NAME}.pdf-{page}-{IMAGE_NUMBER}.png"
    # We need to rename these to match our format while maintaining figure number sequence
    print("\nProcessing to_markdown images...")
    for page_num in pages:
        figures_on_page = set()

        # Get existing figure numbers for this page
        for file in output_dir.glob(f"page_{page_num}_figure_*.png"):
            try:
                figure_num = int(re.search(r'figure_(\d+)', file.name).group(1))
                figures_on_page.add(figure_num)
            except (AttributeError, ValueError):
                continue

        next_figure_num = max(figures_on_page, default=0) + 1

        # Find and rename to_markdown images for this page
        pdf_name = Path(pdf_path).stem
        for file in output_dir.glob(f"{pdf_name}.pdf-{page_num - 1}-*.png"):
            try:
                new_name = f"page_{page_num}_figure_{next_figure_num}.png"
                new_path = output_dir / new_name

                # Rename file
                file.rename(new_path)
                # print(f"Renamed {file.name} to {new_name}")
                next_figure_num += 1

            except Exception as e:
                print(f"Error renaming {file.name}: {str(e)}")
                continue

    return {
        "pages_processed": len(pages),
        "output_directory": str(output_dir),
        "markdown_text": md_text
    }


def is_almost_same_rect(rect1: fitz.Rect, rect2: tuple, tolerance: float = 1.0) -> bool:
    """
    Check if two rectangles are approximately the same, allowing for small differences.

    Args:
        rect1: First rectangle (fitz.Rect)
        rect2: Second rectangle as tuple (x0, y0, x1, y1)
        tolerance: Maximum allowed difference in any coordinate

    Returns:
        bool: True if rectangles are approximately the same
    """
    x0, y0, x1, y1 = rect2
    return (abs(rect1.x0 - x0) <= tolerance and
            abs(rect1.y0 - y0) <= tolerance and
            abs(rect1.x1 - x1) <= tolerance and
            abs(rect1.y1 - y1) <= tolerance)


def extract_clustered_figures(
        pdf_path: str,
        page_number: int,
        output_dir: str = "pdf_images_test",
        black_threshold: float = 0.3,
        white_threshold: float = 0.6,
        y0_threshold: float = 105,
        min_cluster_size: float = 100,
        rect_tolerance: float = 1.0  # Tolerance for rectangle comparison
):
    """
    Extract figures using PyMuPDF's cluster_drawings while filtering out tables.

    Args:
        pdf_path: Path to PDF file
        page_number: Page number to process
        output_dir: Directory to save extracted figures
        black_threshold: Maximum allowed black pixel density (0-1)
        white_threshold: Maximum allowed white pixel density (0-1)
        y0_threshold: Minimum y-coordinate to exclude headers
        min_cluster_size: Minimum size for a cluster to be considered valid
        rect_tolerance: Tolerance for rectangle comparison
    """
    output_path = Path(output_dir).resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    # Thresholds for black and white pixel detection
    BLACK_PIXEL_VALUE = 0
    WHITE_PIXEL_VALUE = 300

    try:
        doc = fitz.open(pdf_path)
        page = doc[page_number - 1]

        # Get tables and their bounding boxes
        tables = page.find_tables()
        table_rects = [table.bbox for table in tables] if tables else []

        # Get clustered drawings
        clusters = page.cluster_drawings()
        if not clusters:
            doc.close()
            return

        figures_analyzed = 0
        figures_saved = 0
        tables_filtered = 0

        # Process each cluster
        for idx, cluster_rect in enumerate(clusters, 1):
            # Skip clusters that are too small or in the header area
            if (cluster_rect.height < min_cluster_size or
                    cluster_rect.width < min_cluster_size or
                    cluster_rect.y0 < y0_threshold):
                continue

            # print(f"\nAnalyzing cluster {idx}: {cluster_rect}")

            # Check if cluster matches any table
            is_table = False
            for i, table_rect in enumerate(table_rects, 1):
                if is_almost_same_rect(cluster_rect, table_rect, rect_tolerance):
                    # print(f"Cluster {idx} matches Table {i}")
                    tables_filtered += 1
                    is_table = True
                    break

            if is_table:
                continue

            # Add padding to the cluster rectangle
            padding = 2
            bounds = fitz.Rect(
                cluster_rect.x0 - padding,
                cluster_rect.y0 - padding,
                cluster_rect.x1 + padding,
                cluster_rect.y1 + padding
            )

            # Create high-resolution pixmap
            pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=bounds)

            # Convert pixmap to numpy array for analysis
            img_data = np.frombuffer(pix.samples, dtype=np.uint8)
            img_data = img_data.reshape(pix.height, pix.width, pix.n)

            # Convert to grayscale
            if pix.n == 4:  # RGBA
                gray_data = np.mean(img_data[:, :, :3], axis=2).astype(np.uint8)
            elif pix.n == 3:  # RGB
                gray_data = np.mean(img_data, axis=2).astype(np.uint8)
            else:
                gray_data = img_data

            # Calculate densities
            total_pixels = gray_data.size
            black_pixels = np.sum(gray_data <= BLACK_PIXEL_VALUE)
            white_pixels = np.sum(gray_data >= WHITE_PIXEL_VALUE)

            black_density = black_pixels / total_pixels
            white_density = white_pixels / total_pixels

            figures_analyzed += 1

            # Save if passes density thresholds
            if black_density <= black_threshold and white_density <= white_threshold:
                image_path = output_path / f"page_{page_number}_figure_{idx}.png"
                pix.save(str(image_path))
                figures_saved += 1
                # print(f"Saved cluster {idx} to {image_path}")

        # print(f"\nAnalysis Summary for Page {page_number}:")
        # print(f"Tables found: {len(table_rects)}")
        # print(f"Total clusters analyzed: {figures_analyzed}")
        # print(f"Tables filtered out: {tables_filtered}")
        # print(f"Clusters saved: {figures_saved}")

        doc.close()
        return {
            'analyzed': figures_analyzed,
            'saved': figures_saved,
            'tables_filtered': tables_filtered
        }

    except Exception as e:
        print(f"Error processing page {page_number}: {str(e)}")
        if 'doc' in locals():
            doc.close()
        return None


def get_all_pdf_documents(dir: str) -> List[str]:
    all_pdf_files = list()
    for file in os.listdir(dir):
        if file.endswith(".pdf"):
            all_pdf_files.append(os.path.join(dir, file))

    return all_pdf_files


def safe_rename(old_path: Path, new_path: Path) -> bool:
    """
    Safely rename a file, handling existing files.

    Returns:
        bool: True if rename was successful
    """
    try:
        if old_path == new_path:
            return True

        if new_path.exists():
            # If target exists, try to find a new unique name
            base = new_path.stem
            ext = new_path.suffix
            counter = 1
            while new_path.exists():
                new_path = new_path.parent / f"{base}_{counter}{ext}"
                counter += 1

        old_path.rename(new_path)
        return True
    except Exception as e:
        print(f"Error renaming {old_path} to {new_path}: {str(e)}")
        return False


def organize_images(output_dir: str, duplicates_dir: str = None) -> Dict[str, List[str]]:
    """
    Optimized version of image organization function.
    Maintains same functionality with improved performance.
    """
    output_dir = Path(output_dir)
    if duplicates_dir:
        duplicates_dir = Path(duplicates_dir)
        duplicates_dir.mkdir(parents=True, exist_ok=True)

    stats = {
        "duplicates_removed": [],
        "renamed_files": [],
        "errors": []
    }

    try:
        # Get all PNG files and create initial data structures
        png_files = list(output_dir.glob("*.png"))
        if not png_files:
            print("No PNG files found in directory")
            return stats

        # Pre-process file information to avoid repeated operations
        file_info = {}
        for file in png_files:
            # Pre-compile regex pattern
            correct_format_pattern = re.compile(r"page_(\d+)_figure_\d+\.png")

            # Pre-process page numbers and format information
            is_correct_format = bool(correct_format_pattern.match(file.name))
            page_num = None

            if "-" in file.stem:
                try:
                    parts = file.stem.split("-")
                    page_num = int(parts[-2]) + 1  # Convert 0-indexed to 1-indexed
                except (ValueError, IndexError):
                    continue
            elif is_correct_format:
                page_num = int(correct_format_pattern.match(file.name).group(1))

            file_info[file] = {
                "is_correct_format": is_correct_format,
                "page_num": page_num,
                "hash": None  # Will be computed only when needed
            }

        print("\nChecking for duplicate images...")
        duplicates = set()
        file_list = list(file_info.keys())

        # Optimize duplicate checking by computing hashes only when needed
        for i, file1 in tqdm(enumerate(file_list)):
            if file1 in duplicates:
                continue

            # Get or compute hash for file1
            if file_info[file1]["hash"] is None:
                with Image.open(file1) as img1:
                    file_info[file1]["hash"] = imagehash.average_hash(img1)

            for file2 in file_list[i + 1:]:
                if file2 in duplicates:
                    continue

                # Get or compute hash for file2
                if file_info[file2]["hash"] is None:
                    with Image.open(file2) as img2:
                        file_info[file2]["hash"] = imagehash.average_hash(img2)

                # Compare hashes
                if (file_info[file1]["hash"] - file_info[file2]["hash"]) / len(
                        file_info[file1]["hash"].hash) ** 2 <= 0.03:
                    # Keep file with correct format
                    if file_info[file2]["is_correct_format"] and not file_info[file1]["is_correct_format"]:
                        duplicates.add(file1)
                        stats["duplicates_removed"].append(str(file1))
                    else:
                        duplicates.add(file2)
                        stats["duplicates_removed"].append(str(file2))

        # Handle duplicates
        for dup in duplicates:
            try:
                if duplicates_dir:
                    shutil.move(str(dup), str(duplicates_dir / dup.name))
                    print(f"Moved duplicate to {duplicates_dir / dup.name}")
                else:
                    os.remove(dup)
                    print(f"Removed duplicate: {dup}")
            except Exception as e:
                print(f"Error handling duplicate {dup}: {str(e)}")
                stats["errors"].append(str(dup))

        # Use dictionary for O(1) lookup of remaining files
        remaining_files = {f for f in png_files if f not in duplicates}

        # Use defaultdict to automatically initialize lists
        from collections import defaultdict
        page_files = defaultdict(list)

        # Organize files by page using pre-processed information
        for file in remaining_files:
            info = file_info[file]
            if info["page_num"] is not None:
                page_files[info["page_num"]].append(file)

        # Rename files
        # print("\nRenaming files with sequential figure numbers...")
        for page_num, files in sorted(page_files.items()):
            for idx, file in enumerate(sorted(files, key=lambda x: x.name), 1):
                new_name = f"page_{page_num}_figure_{idx}.png"
                new_path = output_dir / new_name

                if safe_rename(file, new_path):
                    stats["renamed_files"].append((str(file), new_name))
                    print(f"Renamed {file.name} to {new_name}")
                else:
                    stats["errors"].append(str(file))

        print("\nProcessing complete!")
        print(f"Total files processed: {len(png_files)}")
        print(f"Duplicates handled: {len(stats['duplicates_removed'])}")
        print(f"Files renamed: {len(stats['renamed_files'])}")
        print(f"Errors encountered: {len(stats['errors'])}")

        return stats

    except Exception as e:
        print(f"Error organizing images: {str(e)}")
        stats["errors"].append(str(e))
        return stats


def is_content_image(image_data: bytes, min_color_variance: float = 0.05) -> bool:
    """
    Check if an image contains meaningful content vs being a solid/gradient background.

    Args:
        image_data: Raw image bytes
        min_color_variance: Minimum required color variance (0-1)

    Returns:
        bool: True if image likely contains content, False if likely background
    """
    try:
        # Convert bytes to PIL Image
        import io
        from PIL import Image
        import numpy as np

        # Load image
        img = Image.open(io.BytesIO(image_data))

        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Convert to numpy array
        img_array = np.array(img)

        # Calculate variance metrics
        color_variance = np.var(img_array, axis=(0, 1)).mean() / 255.0

        # Calculate unique colors ratio
        unique_colors = len(np.unique(img_array.reshape(-1, 3), axis=0))
        total_pixels = img_array.shape[0] * img_array.shape[1]
        color_ratio = unique_colors / total_pixels

        return color_variance > min_color_variance and color_ratio > 0.01

    except Exception as e:
        print(f"Error analyzing image content: {str(e)}")
        return True  # Default to keeping image if analysis fails


def extract_all_page_images(pdf_path: str, page_number: int, output_dir: str):
    doc = fitz.open(pdf_path)
    page = doc[page_number - 1]

    # Get list of all images on page
    image_list = page.get_images()

    # Extract each image
    for img_index, img in enumerate(image_list, start=1):
        xref = img[0]  # get the XREF of the image
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]

        # Save image
        output_path = Path(output_dir) / f"page_{page_number}_image_{img_index}.png"
        with open(output_path, "wb") as f:
            f.write(image_bytes)

    doc.close()


def analyze_image_characteristics(directory: Union[str, Path], output_csv: str = "image_analysis.csv") -> pd.DataFrame:
    """
    Analyze images in a directory for various characteristics to identify patterns in background/solid images.

    Args:
        directory: Path to directory containing images
        output_csv: Path to save analysis results

    Returns:
        DataFrame containing image characteristics
    """
    import pandas as pd
    from PIL import Image
    import numpy as np
    from pathlib import Path

    directory = Path(directory)
    data = []

    # Get all PNG files
    image_files = list(directory.glob("*.png"))
    print(f"Found {len(image_files)} images to analyze")

    for img_path in tqdm(image_files, desc="Analyzing images"):
        try:
            # Load image
            img = Image.open(img_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Convert to numpy array
            img_array = np.array(img)

            # Basic characteristics
            width, height = img.size
            aspect_ratio = width / height
            total_pixels = width * height

            # Color analysis
            color_variance = np.var(img_array, axis=(0, 1)).mean() / 255.0
            unique_colors = len(np.unique(img_array.reshape(-1, 3), axis=0))
            color_ratio = unique_colors / total_pixels

            # Color distribution
            mean_color = np.mean(img_array, axis=(0, 1))
            median_color = np.median(img_array, axis=(0, 1))

            # Edge detection to measure complexity
            from scipy import ndimage
            gray = np.mean(img_array, axis=2)
            edges = ndimage.sobel(gray)
            edge_density = np.mean(np.abs(edges)) / 255.0

            # Analyze color bands separately
            color_bands = {
                'red': img_array[:, :, 0],
                'green': img_array[:, :, 1],
                'blue': img_array[:, :, 2]
            }

            band_stats = {}
            for band_name, band_data in color_bands.items():
                band_stats.update({
                    f'{band_name}_mean': np.mean(band_data),
                    f'{band_name}_std': np.std(band_data),
                    f'{band_name}_unique': len(np.unique(band_data))
                })

            # Calculate entropy (measure of randomness/information)
            from scipy.stats import entropy
            hist, _ = np.histogram(gray, bins=256, density=True)
            image_entropy = entropy(hist[hist > 0])

            # Collect all metrics
            metrics = {
                'filename': img_path.name,
                'width': width,
                'height': height,
                'aspect_ratio': aspect_ratio,
                'total_pixels': total_pixels,
                'color_variance': color_variance,
                'unique_colors': unique_colors,
                'color_ratio': color_ratio,
                'edge_density': edge_density,
                'entropy': image_entropy,
                'mean_r': mean_color[0],
                'mean_g': mean_color[1],
                'mean_b': mean_color[2],
                'median_r': median_color[0],
                'median_g': median_color[1],
                'median_b': median_color[2],
                **band_stats
            }

            data.append(metrics)

        except Exception as e:
            print(f"Error processing {img_path.name}: {str(e)}")
            continue

    # Create DataFrame
    df = pd.DataFrame(data)

    # Add derived metrics
    df['color_uniformity'] = 1 - df['color_variance']
    df['is_likely_background'] = (
            (df['color_variance'] < 0.05) &
            (df['edge_density'] < 0.05) &
            (df['entropy'] < 3.0)
    )

    # Save results
    df.to_csv(output_csv, index=False)

    # Print summary statistics
    print("\nSummary of potentially background images:")
    background_images = df[df['is_likely_background']]
    print(f"Found {len(background_images)} likely background images")

    if len(background_images) > 0:
        print("\nCharacteristics of background images:")
        print(background_images.describe())

        print("\nSample of identified background images:")
        print(background_images['filename'].head())

    return df


def plot_image_characteristics(df: pd.DataFrame, output_dir: Union[str, Path] = None):
    """
    Create comprehensive visualizations of image characteristics using matplotlib.
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    from matplotlib.gridspec import GridSpec

    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    # Use a basic style
    plt.style.use('default')

    # Set global style parameters
    plt.rcParams['figure.figsize'] = [12, 8]
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.grid'] = True

    # 1. Distribution plots of key metrics
    fig = plt.figure(figsize=(15, 12))
    gs = GridSpec(2, 2, figure=fig)
    fig.suptitle('Distribution of Key Image Characteristics', fontsize=16, y=0.95)

    # Color variance distribution
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.hist(df['color_variance'], bins=50, alpha=0.7, color='skyblue')
    ax1.axvline(0.05, color='red', linestyle='--', label='Threshold')
    ax1.set_title('Color Variance Distribution')
    ax1.set_xlabel('Color Variance')
    ax1.set_ylabel('Count')
    ax1.legend()

    # Edge density distribution
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.hist(df['edge_density'], bins=50, alpha=0.7, color='lightgreen')
    ax2.axvline(0.05, color='red', linestyle='--', label='Threshold')
    ax2.set_title('Edge Density Distribution')
    ax2.set_xlabel('Edge Density')
    ax2.set_ylabel('Count')
    ax2.legend()

    # Entropy distribution
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.hist(df['entropy'], bins=50, alpha=0.7, color='salmon')
    ax3.axvline(3.0, color='red', linestyle='--', label='Threshold')
    ax3.set_title('Image Entropy Distribution')
    ax3.set_xlabel('Entropy')
    ax3.set_ylabel('Count')
    ax3.legend()

    # Color ratio distribution
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.hist(df['color_ratio'], bins=50, alpha=0.7, color='purple')
    ax4.set_title('Color Ratio Distribution')
    ax4.set_xlabel('Color Ratio')
    ax4.set_ylabel('Count')

    plt.tight_layout()
    if output_dir:
        plt.savefig(output_dir / 'distributions.png', dpi=300, bbox_inches='tight')
    plt.show()

    # 2. Size distribution with background probability
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(df['width'], df['height'],
                          c=df['is_likely_background'],
                          cmap='coolwarm',
                          alpha=0.6)
    plt.colorbar(scatter, label='Background Probability')
    plt.xlabel('Width (pixels)')
    plt.ylabel('Height (pixels)')
    plt.title('Image Size Distribution (colored by background probability)')
    if output_dir:
        plt.savefig(output_dir / 'size_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()

    # 3. Color characteristics
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Color Channel Distributions', fontsize=16)

    channels = ['red', 'green', 'blue']
    colors = ['red', 'green', 'blue']

    for i, (channel, color) in enumerate(zip(channels, colors)):
        mean_key = f'{channel}_mean'
        std_key = f'{channel}_std'

        axes[i].scatter(df[mean_key], df[std_key], alpha=0.5, c=color)
        axes[i].set_title(f'{channel.capitalize()} Channel')
        axes[i].set_xlabel('Mean Value')
        axes[i].set_ylabel('Standard Deviation')
        axes[i].grid(True)

    plt.tight_layout()
    if output_dir:
        plt.savefig(output_dir / 'color_characteristics.png', dpi=300, bbox_inches='tight')
    plt.show()

    # 4. Background characteristics comparison
    fig, ax = plt.subplots(figsize=(12, 6))
    metrics = ['color_variance', 'edge_density', 'entropy']

    background = df[df['is_likely_background']]
    non_background = df[~df['is_likely_background']]

    positions = np.arange(len(metrics))
    width = 0.35

    ax.bar(positions - width / 2,
           [background[m].mean() for m in metrics],
           width,
           label='Background Images',
           color='lightgray',
           alpha=0.7)

    ax.bar(positions + width / 2,
           [non_background[m].mean() for m in metrics],
           width,
           label='Content Images',
           color='skyblue',
           alpha=0.7)

    ax.set_xticks(positions)
    ax.set_xticklabels(metrics, rotation=45)
    ax.set_title('Average Characteristics: Background vs Content Images')
    ax.legend()

    plt.tight_layout()
    if output_dir:
        plt.savefig(output_dir / 'background_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()


def analyze_and_visualize(
        directory: Union[str, Path],
        output_dir: Union[str, Path] = None,
        analyze: bool = True
) -> Optional[pd.DataFrame]:
    """
    Wrapper function to analyze images and create visualizations.

    Args:
        directory: Directory containing images
        output_dir: Directory to save analysis and plots
        analyze: Whether to perform new analysis or load existing

    Returns:
        DataFrame with analysis results
    """
    directory = Path(directory)
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    # Analysis
    if analyze:
        df = analyze_image_characteristics(
            directory=directory,
            output_csv=output_dir / 'image_analysis.csv' if output_dir else 'image_analysis.csv'
        )
    else:
        # Load existing analysis
        try:
            df = pd.read_csv(output_dir / 'image_analysis.csv')
        except FileNotFoundError:
            print("No existing analysis found. Setting analyze=True to create new analysis.")
            return analyze_and_visualize(directory, output_dir, analyze=True)

    # Create visualizations
    plot_image_characteristics(df, output_dir)

    return df


def identify_background_images(df: pd.DataFrame,
                               color_variance_threshold: float = 0.025,  # Stricter than original
                               edge_density_threshold: float = 0.025,  # Based on distribution
                               entropy_threshold: float = 2.5,  # Stricter than original
                               color_uniformity_threshold: float = 0.975  # Based on your stats
                               ) -> List[str]:
    """
    Identify background images using multiple criteria.
    """
    background_mask = (
            (df['color_variance'] < color_variance_threshold) &
            (df['edge_density'] < edge_density_threshold) &
            (df['entropy'] < entropy_threshold) &
            (df['color_uniformity'] > color_uniformity_threshold) &
            # Additional size-based criteria
            (df['width'] < 150) &  # Based on your statistics
            (df['height'] < 100)  # Based on your statistics
    )

    # Get filenames of background images
    background_files = df[background_mask]['filename'].tolist()

    print(f"Identified {len(background_files)} background images")
    print("\nCharacteristics of identified background images:")
    print(df[background_mask][['color_variance', 'edge_density', 'entropy', 'color_uniformity']].describe())

    return background_files

# Example usage
if __name__ == "__main__":
    pdf_dir = r"C:\Users\Anwender\Desktop\Nicolas\Dokumente\FH Bielefeld\Optimierung und Simulation\4. Semester\masterthesis\programming\data\pdf_documents"

    pdf_path = r"C:\Users\Anwender\Desktop\Nicolas\Dokumente\FH Bielefeld\Optimierung und Simulation\4. Semester\masterthesis\programming\data\pdf_documents\ABB-Roboter.pdf"
    output_dir = r"C:\Users\Anwender\Desktop\Nicolas\Dokumente\FH Bielefeld\Optimierung und Simulation\4. Semester\masterthesis\programming\extracted_figures_all"
    output_dir_test = r"C:\Users\Anwender\Desktop\Nicolas\Dokumente\FH Bielefeld\Optimierung und Simulation\4. Semester\masterthesis\programming\pdf_images_test"
    output_dir_temp = r"C:\Users\Anwender\Downloads\temp"

    background_images_path = r"C:\Users\Anwender\Downloads\temp"

    df = pd.read_csv("image_analysis.csv")

    identify_background_images(df)

    # df = analyze_and_visualize(
    #     directory=background_images_path,
    #     output_dir="analysis_output",
    #     analyze=True  # Set to False to use existing analysis
    # )

    # extract_clustered_figures(pdf_path, 30, output_dir_test)

    extract_all_figures(
        pdf_path=pdf_path,
        output_dir=output_dir_test,
        black_threshold=0.3,
        white_threshold=0.6,
        y0_threshold=105,
        min_cluster_size=100,
        dpi=200
    )
    #
    # # extract_all_page_images(pdf_path, 448, output_dir_temp)
    #
    # # After running both extraction methods:
    # stats = organize_images(output_dir_test, r"C:\Users\Anwender\Downloads\temp")
    #
    # # Check results
    # print("\nDuplicates removed:")
    # for dup in stats["duplicates_removed"]:
    #     print(f"- {dup}")
    #
    # print("\nFiles renamed:")
    # for old, new in stats["renamed_files"]:
    #     print(f"- {old} -> {new}")

    all_pdf_files = get_all_pdf_documents(pdf_dir)

    # for pdf_file in tqdm(all_pdf_files):
    #     if "mill" in pdf_file:
    #         print(f"Processing {pdf_file}...")
    #         output_dir = os.path.join(output_dir, Path(pdf_file).stem)
    #
    #         extract_all_figures(
    #             pdf_path=pdf_file,
    #             output_dir=output_dir,
    #             black_threshold=0.3,
    #             white_threshold=0.6,
    #             y0_threshold=105,
    #             min_cluster_size=100,
    #             dpi=200,
    #             graphics_limit=100
    #         )
    #
    #         stats = organize_images(output_dir)
    #
    #         output_dir = r"C:\Users\Anwender\Desktop\Nicolas\Dokumente\FH Bielefeld\Optimierung und Simulation\4. Semester\masterthesis\programming\extracted_figures_all"
    #
