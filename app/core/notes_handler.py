import json

class DataSender:
    def __init__(self):
        self.notes_file_path = 'app\\assets\\data\\notes.json'

    def send_data(self, calendar, topic, description, file_path):
        data = self._read_notes()
        notes = data['notes']
        note_found = self._update_existing_note_if_present(notes, calendar.text, topic.text, description.text)
        
        if not note_found:
            self._add_new_note(notes, calendar.text, topic.text, description.text, file_path)
        
        self._write_notes(data)

    def _read_notes(self):
        try:
            with open(self.notes_file_path, 'r') as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            raise Exception(f"File {self.notes_file_path} not found.")
        except json.JSONDecodeError:
            raise Exception("Error decoding JSON from the file.")

    def _update_existing_note_if_present(self, notes, date, title, description):
        for note in notes:
            if note['date'] == date:
                if title == note['title'] and description == note['description']:
                    return True
                elif title != note['title'] or description != note['description']:
                    note['title'] = title
                    note['description'] = description
                    #notes.remove(note)
                    return True
        return False

    def _add_new_note(self, notes, date, title, description, file_path):
        new_note = {
            "date": date,
            "title": title,
            "description": description,
            "filePath": file_path
        }
        notes.append(new_note)

    def _write_notes(self, data):
        try:
            with open(self.notes_file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
        except IOError:
            raise Exception("Error writing JSON to the file.")