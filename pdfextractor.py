import textract
import re


def readFile(filename):
    content = textract.process(filename, method='pdfminer')
    return content.decode('utf-8')


def writeToCSV(bill_list, order):
    f = open('output.csv', 'w')
    lines = []
    for fact in bill_list:
        line = ''
        for field in order:
            line += str(fact[field]) + '\t'
        lines.append(line + '\n')
    print(lines)
    f.writelines(lines)
    f.close()
    return True


def extractInfo(filename):
    bill = {'Numéro Facture': None, 'Date': None, 'Libélé Désignation': '', 'Prix HT': 0, 'TVA': 0,
            'Prix TTC': 0, 'Nom du client': ''}
    r = (readFile(filename)).split('\n')
    print(r)
    items = 0
    for i in range(len(r)):
        ri = r[i]
        if ri.startswith('FACTURE'):
            find = re.search(r'\d+$', ri)
            if find is not None:
                bill['Numéro Facture'] = find.group(0)
                items += 1
        elif ri.lower().startswith('date de facturation'):
            find = re.search(r'\d{2}\/\d{2}\/\d{4}$', ri)
            if find is not None:
                bill['Date'] = find.group(0)
            items += 1
        elif ri == 'Total HT':
            jump = 0
            if r[i+1] == '':
                jump = 1
            if r[i + 1 + jump] == 'Total Net TTC':
                # Extract HT price
                ht = r[i + 3 + 3*jump]
                found = re.search(r'\d+,\d+', ht)
                bill['Prix HT'] = found.group(0)
                # Extract TTC price
                ttc = r[i + 4 + 4*jump]
                found = re.search(r'\d+,\d+', ttc)
                bill['Prix TTC'] = found.group(0)
                # increment the counter
                i += 5
            elif r[i + 2 + 2*jump] == 'Total Net TTC':
                # Extract HT price
                ht = r[i + 4 + 4*jump]
                found = re.search(r'\d+,\d+', ht)
                bill['Prix HT'] = found.group(0)
                # Extract TVA
                tva = r[i + 5 + 5*jump]
                found = re.search(r'\d+,\d+', tva)
                bill['TVA'] = found.group(0)
                # Extract TTC price
                ttc = r[i + 6*jump]
                found = re.search(r'\d+,\d+', ttc)
                bill['Prix TTC'] = found.group(0)
                # increment the counter
                i += 7
            items += 1
        elif ri == 'Description':
            desc = r[i + 2]
            cl_index = 0
            # Extract the end of the client bloc
            if 'facture' in r[i - 2].lower():
                cl_index = i - 4
            else:
                cl_index = i - 2
            # Extract the beginning of the client bloc
            j = cl_index
            while r[j] != '' and j >= 0:
                j -= 1
            # Extract the client name
            print(str(j))
            client_name = r[j + 1]
            if re.search('^\d+', r[j + 2]) is None:
                print('here:' + r[j+2])
                client_name += ' ' + r[j + 2]
            if r[i + 3] != '':
                desc += ' ' + r[i + 3]
            bill['Libélé Désignation'] = desc
            bill['Nom du client'] = client_name
            items += 1
        # if items == 5:
    return bill
