#!/usr/bin/env python
from pathlib import Path
from tqdm import tqdm
import logging
import subprocess
import re

articles = list(Path('content/lessen').rglob('*/index.md'))

for p in tqdm(articles[4:5]):
    bare_html = (Path(str(p).replace("content/",
                                    "public/bare/", 1)
                      .replace("index.md", "index.html")).absolute())
    lesson_html = Path(str(bare_html).replace("public/bare/", "public/",
                                              1)).absolute()

    print(str(bare_html))
    pdf_file = (lesson_html.parent
                / ('-'.join([lesson_html.parent.parent.name, 
                             lesson_html.parent.name]).title() + '.pdf'))
    args = ['wkhtmltopdf', '-T', '25mm', '-B', '25mm', '-R', '25mm', '-L',
            '25mm', '--no-stop-slow-scripts',
            '--javascript-delay', '5000', '--viewport-size', '1920x1080',
            str(bare_html),
            str(pdf_file)]
    child_proccess = subprocess.Popen(args, stdin=subprocess.PIPE)
    # Replace absolute refs by relative refs
    root_dir = Path('public').absolute()
    html_content = bare_html.read_text()
    
    # for match in re.finditer(r'="(/bare/[^"]*)"', html_content):
    #     src_path = match.group(1)
    #     new_src_path = src_path.replace('/bare/', f'{root_dir}/')
    #     print(new_src_path)
    #     print(f'Exists? {Path(new_src_path).exists()}')
                
    child_proccess.stdin.write(html_content.replace('="/bare/', f'="{root_dir}/')
                               .encode('utf-8'))
    child_proccess.communicate()
    child_proccess.stdin.close()
   
    # Link to correct pdf-file by replacing href pattern in lesson html file
    pdf_link = str(pdf_file).replace('public/', '/', 1)
    new_html_content = (lesson_html.read_text()
                        .replace("##REPLACED_BY_CREATE_PDFS##", pdf_link))
    lesson_html.write_text(new_html_content)
