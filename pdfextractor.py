import textract

def readFile(filename):
  content = textract.process(filename, method='pdfminer')
  return content.decode('utf-8')
