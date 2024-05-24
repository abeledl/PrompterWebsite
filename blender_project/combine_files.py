import os


def combine_files(file_list, output_file, main_file):
    import_statements = set()
    from_import_statements = set()
    nltk_statements = set()

    # Extract import statements from the main file
    with open(main_file, 'r') as main_f:
        lines = main_f.readlines()
        for line in lines:
            if line.startswith('import'):
                import_statements.add(line.strip())
            elif line.startswith('from'):
                from_import_statements.add(line.strip())
            elif line.startswith('nltk'):
                nltk_statements.add(line.strip())

    # Use a temporary file for initial combining
    temp_output = output_file + '.tmp'

    with open(temp_output, 'w') as outfile:
        for f_name in file_list:
            with open(f_name, 'r') as infile:
                for line in infile:
                    # Skip import lines from all files except the main file
                    if line.startswith('import') or line.startswith('from') or line.startswith('nltk'):
                        if f_name == main_file:
                            continue  # Skip imports in the main file
                        continue
                    outfile.write(line)
                outfile.write('\n\n')  # Ensure separation between files

    # Now write the final output file with imports at the top
    with open(output_file, 'w') as final_outfile:
        # Write import statements first
        final_outfile.write('\n'.join(sorted(import_statements)) + '\n\n')
        # Write from import statements next
        final_outfile.write('\n'.join(sorted(from_import_statements)) + '\n\n')
        # Write nltk statement
        final_outfile.write('\n'.join(sorted(nltk_statements)) + '\n\n')

        # Write the rest of the combined content
        with open(temp_output, 'r') as temp_file:
            final_outfile.write(temp_file.read())

    # Remove the temporary file
    os.remove(temp_output)


# List your Python files in the order you want them concatenated
files_to_combine = ['font_3d_text_generator.py', 'functions_classes.py', 'main.py']

# Specify the output file
output_filename = 'combined_script.py'

# Specify the main file
_main_file = 'main.py'

combine_files(files_to_combine, output_filename, _main_file)

print(f'Files combined into {output_filename}')
