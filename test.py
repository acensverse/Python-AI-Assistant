import os

def load_conversations():
    chat_dict = {}
    folder_path = 'Openai'

    try:
        # Iterate through files in the Openai folder
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".txt"):
                # Extract conversation ID and timestamp from the file name
                parts = file_name.split("_")
                convo_id = int(parts[1])
                timestamp = parts[2].split(".")[0]

                # Read the content of the text file
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r') as file:
                    content = file.read()

                # Update chat_dict with the conversation details
                chat_dict[convo_id] = {
                    'user_query': content.split("User: ")[1].split("\n")[0].strip(),
                    'ai_response': content.split("AI: ")[1].strip(),
                    'timestamp': timestamp
                }

        return chat_dict

    except FileNotFoundError:
        # Return an empty dictionary if no saved conversations are found
        return {}

# Initialize chat dictionary
chatDict = load_conversations()

# Print existing conversation IDs
print("Existing Conversation IDs:", list(chatDict.keys()))
