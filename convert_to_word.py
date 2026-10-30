import pypandoc

input_file = 'reports/final/CYC386_SecureShare_Final_Report.md'
output_file = 'reports/final/CYC386_SecureShare_Final_Report.docx'

print("Downloading Pandoc (this may take a moment)...")
pypandoc.download_pandoc()
print("Pandoc downloaded successfully!")

print(f"Converting {input_file} to {output_file}...")
pypandoc.convert_file(input_file, 'docx', outputfile=output_file)
print("Conversion complete!")
print(f"Word file saved to: {output_file}")
