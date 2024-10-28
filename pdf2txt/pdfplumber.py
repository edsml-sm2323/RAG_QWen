import re
import pdfplumber
import os

class PDFTextExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    # 通过表格的top和bottom来读取页面的文章
    def check_lines(self, page, top, bottom):
        try:
            lines = page.extract_words()
        except Exception as e:
            print(f'页码: {page.page_number}, 抽取文本异常，异常信息: {e}')
            return ''
        # 正则表达式检查
        check_re = '(?:。|；|单位：元|单位：万元|币种：人民币)$'
        page_top_re = '(招股意向书(?:全文)?(?:（修订版）|（修订稿）|（更正后）)?)'

        text = ''
        last_top = 0
        last_check = 0
        if top == '' and bottom == '':
            if len(lines) == 0:
                print(f'{page.page_number}页无数据, 请检查！')
                return ''
        for l in range(len(lines)):
            each_line = lines[l]
            if top == '' and bottom == '':
                if abs(last_top - each_line['top']) <= 2:
                    text = text + each_line['text']
                elif last_check > 0 and (page.height * 0.9 - each_line['top']) > 0 and not re.search(check_re, text):
                    if '\n' not in text and re.search(page_top_re, text):
                        text = text + '\n' + each_line['text']
                    else:
                        text = text + each_line['text']
                else:
                    if text == '':
                        text = each_line['text']
                    else:
                        text = text + '\n' + each_line['text']
            elif top == '':
                if each_line['top'] > bottom:
                    if abs(last_top - each_line['top']) <= 2:
                        text = text + each_line['text']
                    elif last_check > 0 and (page.height * 0.85 - each_line['top']) > 0 and not re.search(check_re, text):
                        if '\n' not in text and re.search(page_top_re, text):
                            text = text + '\n' + each_line['text']
                        else:
                            text = text + each_line['text']
                    else:
                        if text == '':
                            text = each_line['text']
                        else:
                            text = text + '\n' + each_line['text']
            else:
                if top > each_line['top'] > bottom:
                    if abs(last_top - each_line['top']) <= 2:
                        text = text + each_line['text']
                    elif last_check > 0 and (page.height * 0.85 - each_line['top']) > 0 and not re.search(check_re, text):
                        if '\n' not in text and re.search(page_top_re, text):
                            text = text + '\n' + each_line['text']
                        else:
                            text = text + each_line['text']
                    else:
                        if text == '':
                            text = each_line['text']
                        else:
                            text = text + '\n' + each_line['text']
            last_top = each_line['top']
            last_check = each_line['x1'] - page.width * 0.83

        return text

    # 删除没有数据的列
    def drop_empty_cols(self, data):
        transposed_data = list(map(list, zip(*data)))
        filtered_data = [col for col in transposed_data if not all(cell == '' for cell in col)]
        result = list(map(list, zip(*filtered_data)))
        return result

    # 提取页面中的文本和表格
    def extract_text_and_tables(self, page):
        all_text = ""
        bottom = 0
        try:
            tables = page.find_tables()
        except:
            tables = []
        if len(tables) >= 1:
            count = len(tables)
            for table in tables:
                if table.bbox[3] < bottom:
                    pass
                else:
                    count -= 1
                    top = table.bbox[1]

                    text = self.check_lines(page, top, bottom)
                    text_list = text.split('\n')
                    for _t in range(len(text_list)):
                        all_text += text_list[_t] + '\n'

                    bottom = table.bbox[3]
                    new_table = table.extract()
                    r_count = 0
                    for r in range(len(new_table)):
                        row = new_table[r]
                        if row[0] is None:
                            r_count += 1
                            for c in range(len(row)):
                                if row[c] is not None and row[c] not in ['', ' ']:
                                    if new_table[r - r_count][c] is None:
                                        new_table[r - r_count][c] = row[c]
                                    else:
                                        new_table[r - r_count][c] += row[c]
                                    new_table[r][c] = None
                        else:
                            r_count = 0

                    end_table = []
                    for row in new_table:
                        if row[0] is not None:
                            cell_list = []
                            cell_check = False
                            for cell in row:
                                if cell is not None:
                                    cell = cell.replace('\n', '')
                                else:
                                    cell = ''
                                if cell != '':
                                    cell_check = True
                                cell_list.append(cell)
                            if cell_check:
                                end_table.append(cell_list)
                    end_table = self.drop_empty_cols(end_table)

                    markdown_table = ''
                    for i, row in enumerate(end_table):
                        row = [cell for cell in row if cell is not None and cell != '']
                        processed_row = [str(cell).strip() if cell is not None else "" for cell in row]
                        markdown_row = '| ' + ' | '.join(processed_row) + ' |\n'
                        markdown_table += markdown_row
                        if i == 0:
                            separators = [':---' if cell.isdigit() else '---' for cell in row]
                            markdown_table += '| ' + ' | '.join(separators) + ' |\n'
                    all_text += markdown_table + '\n'

                    if count == 0:
                        text = self.check_lines(page, '', bottom)
                        text_list = text.split('\n')
                        for _t in range(len(text_list)):
                            all_text += text_list[_t] + '\n'

        else:
            text = self.check_lines(page, '', '')
            text_list = text.split('\n')
            for _t in range(len(text_list)):
                all_text += text_list[_t] + '\n'

        return all_text

    # 提取整个PDF的文本
    def extract_text(self):
        with pdfplumber.open(self.pdf_path) as pdf:
            all_text = ""
            for page in pdf.pages:
                all_text += self.extract_text_and_tables(page)
        return all_text

    # 保存提取的文本到文件
    def save_text_to_file(self, save_path):
        extracted_text = self.extract_text()
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(extracted_text)
        print(f"文本保存到: {save_path}")

# 使用示例
if __name__ == "__main__":
    # 批量处理PDF文件并保存为TXT文件
    def process_pdf_folder(pdf_folder, output_folder):
        # 遍历PDF文件夹中的所有PDF文件
        for filename in os.listdir(pdf_folder):
            if filename.endswith(".pdf") or filename.endswith(".PDF"):  # 过滤PDF文件
                pdf_path = os.path.join(pdf_folder, filename)
                # 去除文件扩展名，作为TXT文件的名称
                txt_filename = os.path.splitext(filename)[0] + ".txt"
                txt_path = os.path.join(output_folder, txt_filename)

                # 处理PDF文件并保存为TXT
                extractor = PDFTextExtractor(pdf_path)
                extractor.save_text_to_file(txt_path)

                print(f"已处理: {filename}, 保存为: {txt_filename}")


    # 文件夹路径
    pdf_folder_path = "data/pdf"  # 存放PDF文件的文件夹路径
    output_folder_path = "data/pdf2txt"  # 存放TXT文件的输出文件夹路径

    # 执行批量处理
    process_pdf_folder(pdf_folder_path, output_folder_path)