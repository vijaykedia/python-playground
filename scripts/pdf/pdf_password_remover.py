import argparse
from pypdf import PdfReader, PdfWriter

def parse_args():
    arguments = argparse.ArgumentParser()
    arguments.add_argument('-i', '--input', help='Input PDF file')
    arguments.add_argument('-p', '--password', help='Password for the PDF file')
    arguments.add_argument('-o', '--output', required=False, help='Output PDF file')
    return arguments.parse_known_args()

def decrypt_pdf(input_file, output_file, password = '') -> None:
    reader = PdfReader(input_file)
    if reader.is_encrypted:
        reader.decrypt(password)
    writer = PdfWriter(clone_from=reader)
    with open(output_file, 'wb') as out:
        writer.write(out)

if __name__ == '__main__':
    args, unknown = parse_args()
    print(args)
    print(unknown)
    assert len(unknown) <= 2
    input_inferred = False
    if args.input is None:
        if len(unknown) > 0:
            args.input = unknown[0]
            input_inferred = True
        else:
            print('Password encoded input pdf file is required')
            exit(1)
    if args.password is None:
        if input_inferred:
            if len(unknown) > 1:
                args.password = unknown[1]
            else:
                print('Password for the input pdf file is required')
                exit(1)
        else:
            if len(unknown) > 0:
                args.password = unknown[0]
            else:
                print('Password for the input pdf file is required')
                exit(1)
    if args.output is None:
        args.output = args.input + '.decoded'
    decrypt_pdf(args.input, args.output, args.password)
