# set_passwords.py
import os
import django

# --- Django setup ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "startup.settings")
django.setup()

from django.contrib.auth.models import User


def set_pw(username, password):
    try:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"✓ Password set for user '{username}'")
    except User.DoesNotExist:
        print(f"✗ User '{username}' not found")


def main():
    print("Setting passwords for seeded users...\n")

    set_pw("david", "davidpass")
    set_pw("sam", "sampass")
    set_pw("librarian", "librarianpass")

    print("\nDone.")


if __name__ == "__main__":
    main()