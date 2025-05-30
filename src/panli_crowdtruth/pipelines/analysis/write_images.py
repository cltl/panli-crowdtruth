import os


def write_images(fig, dir_images, name_file):

    pdf_dir = os.path.join(dir_images, "pdf")
    html_dir = os.path.join(dir_images, "html")
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    if not os.path.exists(html_dir):
        os.makedirs(html_dir)

    pdf_path = os.path.join(pdf_dir, f"{name_file}.pdf")
    fig.write_image(pdf_path)

    html_path = os.path.join(html_dir, f"{name_file}.html")
    fig.write_html(html_path)
