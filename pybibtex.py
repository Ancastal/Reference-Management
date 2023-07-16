class BibTeXEntry:
    def __init__(self, type, id, fields):
        self.type = type
        self.id = id
        self.fields = fields

    def __repr__(self):
        return f"{self.type}(id={self.id}, fields={self.fields})"

    def generate_citation(self):
        type_lower = self.type.lower()
        fields = self.fields

        if type_lower == "misc":
            # Handle miscellaneous entry type
            title = fields.get("title")
            year = fields.get("year", "n.d.")
            url = fields.get("url")

            citation_parts = [part for part in [title, f"({year})", "Retrieved from", url] if part]

        elif type_lower == "inproceedings":
            # Handle inproceedings entry type
            authors = fields.get("author")
            title = fields.get("title")
            booktitle = fields.get("booktitle")
            address = fields.get("address")
            publisher = fields.get("publisher")
            year = fields.get("year")
            pages = fields.get("pages")

            authors_list = authors.split(" and ")
            authors_citation = authors_list[0]
            if len(authors_list) > 1:
                authors_citation += " et al."

            citation_parts = [
                part
                for part in [
                    authors_citation,
                    f"({year}). {title}.",
                    f"In {booktitle}.",
                    f"Pages {pages}." if pages else "",
                    f"{address}: {publisher}." if address and publisher else "",
                ]
                if part
            ]

        elif type_lower == "article":
            # Handle article entry type
            authors = fields.get("author")
            title = fields.get("title")
            journal = fields.get("journal")
            volume = fields.get("volume")
            year = fields.get("year")
            pages = fields.get("pages")

            authors_list = authors.split(" and ")
            authors_citation = authors_list[0]
            if len(authors_list) > 1:
                authors_citation += " et al."

            citation_parts = [
                part
                for part in [
                    authors_citation,
                    f"({year}). {title}.",
                    journal,
                    f"Volume {volume}." if volume else "",
                    f"Pages {pages}." if pages else "",
                ]
                if part
            ]

        else:
            # Handle other entry types
            return "Citation format for this type of entry is not supported."

        citation = " ".join(citation_parts)

        return citation

    def generate_summary(self):
        title = self.fields.get("title")
        from api import search_title
        results = search_title(title)
        if results:
            return results[0]



class BibTeXFile:
    def __init__(self, filename):
        self.filename = filename
        self.entries = self.load_entries()

    def load_entries(self):
        entries = {}
        with open(self.filename, "r") as f:
            content = f.read().split("\n")
            current_entry = None
            for line in content:
                line = line.strip()
                if line.startswith("@"):
                    type, id = line[1:].split("{", 1)
                    type = type.strip()
                    id = id.rstrip(",").strip()
                    current_entry = BibTeXEntry(type, id, {})
                    entries[id] = current_entry
                elif "=" in line and current_entry is not None:
                    field, value = line.split("=", 1)
                    field = field.strip()
                    value = value.rstrip(",").strip().strip("{}")
                    current_entry.fields[field] = value
        return entries

    def get_entry(self, id):
        return self.entries.get(id)

    def add_entry(self, type, id, fields):
        self.entries[id] = BibTeXEntry(type, id, fields)
        self.save()

    def save(self):
        with open(self.filename, "w") as f:
            for entry in self.entries.values():
                f.write(f"@{entry.type}{{{entry.id},\n")
                for field, value in entry.fields.items():
                    f.write(f"    {field} = {{{value}}},\n")
                f.write("}\n")

    def filter_entries(self, field, condition):
        results = []
        for entry in self.entries.values():
            if condition(entry.fields.get(field, '')):
                results.append(entry)
        return results

    def delete_entry(self, id):
        if id in self.entries:
            del self.entries[id]
            self.save()
            return True
        else:
            return False
