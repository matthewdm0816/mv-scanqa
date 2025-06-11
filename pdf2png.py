from pdf2image import convert_from_path
import os

# 转换PDF到PNG
def convert_pdf_figures(pdf_folder='static/pdfs', output_folder='static/images'):
    os.makedirs(output_folder, exist_ok=True)
    
    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            # 转换PDF，DPI越高质量越好
            images = convert_from_path(pdf_path, dpi=600)
            
            # 保存为PNG
            for i, image in enumerate(images):
                output_name = pdf_file.replace('.pdf', f'_page{i+1}.png' if len(images) > 1 else '.png')
                output_path = os.path.join(output_folder, output_name)
                image.save(output_path, 'PNG')
                print(f"Converted {pdf_file} to {output_name}")

# 使用方法
convert_pdf_figures()