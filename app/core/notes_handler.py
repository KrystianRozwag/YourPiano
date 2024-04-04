import json
from core.server_handler import DatabaseLoader
class DataReader:
    def __init__(self):
        self.notes_file_path = 'app\\assets\\data\\notes.json'
    def load_data(self, topic_field, text_input, date):
        data = self._read_notes()
        notes = data['notes']
        db = DatabaseLoader()
        is_connected = db.connect()
        if(is_connected):
            row = db.read_data_from_db(date)
            if(row):
                topic_field.text = row[0]
                text_input.text = row[1]
                print(row)
        else:
            for note in notes:
                if note['date'] == date:
                    topic_field.text = note['title']
                    text_input.text = note['description']
        
    def _read_notes(self):
        try:
            with open(self.notes_file_path, 'r') as json_file: #create file if not found
                return json.load(json_file)
        except FileNotFoundError:
            raise Exception(f"File {self.notes_file_path} not found.")
        except json.JSONDecodeError:
            raise Exception("Error decoding JSON from the file.")
        
class DataSender:
    def __init__(self):
        self.notes_file_path = 'app\\assets\\data\\notes.json'

    def send_data(self, calendar, topic, description, file_path): #maybe here to put sending data to the server
        data = self._read_notes()
        notes = data['notes']
        db = DatabaseLoader()
        is_connected = db.connect()
        if(is_connected):

            row = db.read_data_from_db(calendar.text)
            if(row):
                #note_found = self._update_existing_note_if_present(notes, calendar.text, topic.text, description.text) #update code to update data in the db
                note_found = True
                db.update_data_in_db(topic.text, description.text, file_path, calendar.text)
            else:
                db.send_data_to_db(topic.text, description.text,calendar.text,file_path)
                note_found = False

            db.disconnect()


        #note_found = self._update_existing_note_if_present(notes, calendar.text, topic.text, description.text)
        
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