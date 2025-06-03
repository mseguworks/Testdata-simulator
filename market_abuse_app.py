# Read the content of the file
with open('market_abuse_app.py', 'r', encoding='utf-8') as file:
    content = file.read()

# Replace non-breaking spaces (U+00A0) with standard spaces (U+0020)
cleaned_content = content.replace('\u00a0', ' ')

# Write the cleaned content back to the file
with open('market_abuse_app_cleaned.py', 'w', encoding='utf-8') as file:
    file.write(cleaned_content)

print("The file has been cleaned and saved as 'market_abuse_app_cleaned.py'.")

