import tabula

tables = tabula.read_pdf("PAN Card.pdf", pages="all")
df = tables[0]
print(df)
