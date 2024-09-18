import openai
from dotenv import load_dotenv
import os

# Function to generate application letter using OpenAI

def generate_application_letter(name, p_info, position, comp_name, comp_desc, offer):
    try:
        # Load environment variables from .env file
        load_dotenv()

        # Conversation history and the initial system message
        system_role = f"You are here to help the user to find a job"  # Define system role here
        messages = [{"role": "system", "content": system_role}, {"role": "user", "content": f"Generate an application letter on behalf of: '{name}' - '{p_info}' to apply for the position {position} at the following company: '{comp_name}'. This is a description of the company: '{comp_desc}'. And this is the actual job offer text: {offer}. Write an application letter to the company. Focus on where skillz and strength of the applicant match the requirements of the position and be creative here. Use the language of the offer for the application letter."}]

        # Load the OpenAI API key from a file
        api_key = os.getenv('OPENAI_API_KEY')

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=1.0,
            max_tokens=1000,
        )
            # Append the user's message to the conversation history
        messages.append({"role": "user", "content": f"Generate an application letter on behalf of: '{name}' - '{p_info}' to apply for the position {position} at the following company: '{comp_name}'. This is a description of the company: '{comp_desc}'. And this is the actual job offer text: {offer}. Write an application letter to the company. Focus on where skillz and strength of the applicant match the requirements of the position and be creative here. Use the language of the offer for the application letter."})


        letter = response.choices[0].message.content
        return letter
    except Exception as e:
        print("OpenAI Error", f"Failed to generate application letter.\nError: {e}")
        return None

# Example Data: 

# name = 'Siggi Halfpape'
# p_info = "Ich bin der Siggi Halfpape. Ich bin ganz gut mit Maschinen. Drehmaschinen, das ist so mein Ding. Ich mach das schon lange und weiß, wie man da die Knöpfe drücken muss. Ich bin nicht so der große Denker, aber wenn's um's Drehen geht, da bin ich dabei."
# position = 'Drehmaschinen Lotzi'
# comp_name = 'Horst Schwankowski Metall KG'
# comp_desc = '''
# Horst 'Schwankowski Metall KG' ist ein traditionsreiches Familienunternehmen mit langjähriger 
# Erfahrung in der Metallbearbeitung. Wir sind spezialisiert auf die Herstellung hochwertiger 
# Präzisionsteile für verschiedene Branchen. Unser Unternehmen zeichnet 
# sich durch eine moderne Infrastruktur, ein engagiertes Team und eine hohe Kundenorientierung aus.
# '''
# offer = '''
# Horst 'Schwankowski Metall KG sucht einen engagierten Drehmaschinen Lotzi (m/w/d) für unser hochmodernes Produktionswerk in Kall. Als Drehmaschinen Lotzi sind Sie für die präzise Bearbeitung von Metallteilen auf Drehmaschinen verantwortlich.

# Ihre Aufgaben:

#     Bedienung und Wartung von CNC-Drehmaschinen
#     Einhaltung von Qualitätsstandards und Toleranzen
#     Durchführung von Qualitätskontrollen
#     Optimierung von Arbeitsabläufen'''

# print(generate_application_letter(name, p_info, position, comp_name, comp_desc, offer))
