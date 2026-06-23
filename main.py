import os
import json
import hashlib
from cryptography.fernet import Fernet


class SecureNotesApp:
    def __init__(self):
        self.key_file = "secret.key"
        self.password_file = "master_password.txt"
        self.notes_file = "notes.json"

        self.key = self.load_or_create_key()
        self.cipher = Fernet(self.key)

        self.setup_password()

    def load_or_create_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as file:
                return file.read()

        key = Fernet.generate_key()

        with open(self.key_file, "wb") as file:
            file.write(key)

        return key

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def setup_password(self):
        if not os.path.exists(self.password_file):
            print("Create Master Password")
            password = input("Enter Master Password: ")

            with open(self.password_file, "w") as file:
                file.write(
                    self.hash_password(password)
                )

            print("Master Password Created\n")

    def verify_password(self):
        password = input(
            "Enter Master Password: "
        )

        with open(self.password_file, "r") as file:
            stored_hash = file.read()

        return (
            self.hash_password(password)
            == stored_hash
        )

    def load_notes(self):
        if not os.path.exists(self.notes_file):
            return []

        with open(
            self.notes_file,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    def save_notes(self, notes):
        with open(
            self.notes_file,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(notes, file, indent=4)

    def add_note(self):
        note = input(
            "\nEnter Note:\n"
        )

        encrypted_note = self.cipher.encrypt(
            note.encode()
        ).decode()

        notes = self.load_notes()

        notes.append(encrypted_note)

        self.save_notes(notes)

        print("Note Saved Successfully")

    def view_notes(self):
        notes = self.load_notes()

        if not notes:
            print("\nNo Notes Found")
            return

        print("\nSaved Notes\n")

        for index, note in enumerate(
            notes,
            start=1
        ):
            decrypted_note = self.cipher.decrypt(
                note.encode()
            ).decode()

            print(
                f"{index}. {decrypted_note}"
            )

    def delete_note(self):
        notes = self.load_notes()

        if not notes:
            print("\nNo Notes Available")
            return

        self.view_notes()

        try:
            choice = int(
                input(
                    "\nEnter Note Number To Delete: "
                )
            )

            if 1 <= choice <= len(notes):
                notes.pop(choice - 1)

                self.save_notes(notes)

                print(
                    "Note Deleted Successfully"
                )
            else:
                print("Invalid Selection")

        except ValueError:
            print("Invalid Input")

    def menu(self):
        while True:
            print("\n" + "=" * 40)
            print("SECURE NOTES APPLICATION")
            print("=" * 40)

            print("1. Add Note")
            print("2. View Notes")
            print("3. Delete Note")
            print("4. Exit")

            choice = input(
                "\nEnter Choice: "
            )

            if choice == "1":
                self.add_note()

            elif choice == "2":
                self.view_notes()

            elif choice == "3":
                self.delete_note()

            elif choice == "4":
                print("Goodbye")
                break

            else:
                print("Invalid Choice")


if __name__ == "__main__":
    app = SecureNotesApp()

    if app.verify_password():
        app.menu()
    else:
        print("Incorrect Password")