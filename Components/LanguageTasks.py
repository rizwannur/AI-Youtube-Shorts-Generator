import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

# Configure the Gemini API with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("Gemini API key not found. Make sure GEMINI_API_KEY is defined in the .env file.")


# Function to extract start and end times
def extract_times(json_string):
    try:
        # Parse the JSON string
        data = json.loads(json_string)

        # Extract start and end times as floats
        start_time = float(data[0]["start"])
        end_time = float(data[0]["end"])

        # Convert to integers
        start_time_int = int(start_time)
        end_time_int = int(end_time)
        return start_time_int, end_time_int
    except Exception as e:
        print(f"Error in extract_times: {e}")
        return 0, 0


system = """
Based on the Transcription user provides with start and end, Highlight the main parts in less than 1 min which can be directly converted into a short. highlight it such that its interesting and also keep the time stamps for the clip to start and end. only select a continuous Part of the video

Follow this Format and return in valid json 
[{
start: "Start time of the clip",
content: "Highlight Text",
end: "End Time for the highlighted clip"
}]
it should be one continuous clip as it will then be cut from the video and uploaded as a tiktok video. so only have one start, end and content

Don't say anything else, just return Proper Json. no explanation etc

IF YOU DONT HAVE ONE start AND end WHICH IS FOR THE LENGTH OF THE ENTIRE HIGHLIGHT, THEN 10 KITTENS WILL DIE, I WILL DO JSON['start'] AND IF IT DOESNT WORK THEN...
"""

User = """
Any Example
"""


def GetHighlight(Transcription):
    print("Getting Highlight from Transcription ")
    try:
        # Create a Gemini model instance (using gemini-1.5-pro which is similar to GPT-4o)
        model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
        
        # Configure the generation parameters
        generation_config = {
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        
        # Prepare the prompt
        combined_prompt = f"{system}\n\nTranscription:\n{Transcription}"
        
        # Generate content
        response = model.generate_content(
            combined_prompt,
            generation_config=generation_config
        )

        # Extract the content from the response
        json_string = response.text
        json_string = json_string.replace("json", "")
        json_string = json_string.replace("```", "")
        # print(json_string)
        Start, End = extract_times(json_string)
        if Start == End:
            Ask = input("Error - Get Highlights again (y/n) -> ").lower()
            if Ask == "y":
                Start, End = GetHighlight(Transcription)
        return Start, End
    except Exception as e:
        print(f"Error in GetHighlight: {e}")
        return 0, 0


if __name__ == "__main__":
    print(GetHighlight(User))
