import tkinter as tk
import requests
from bs4 import BeautifulSoup

# Function to fetch lyrics
def fetch_lyrics():
    song_title = title_entry.get()
    artist_name = artist_entry.get()
    
    if not song_title or not artist_name:
        lyrics_text.delete("1.0", tk.END)
        lyrics_text.insert(tk.END, "Please enter both song title and artist name.")
        return
    
    search_url = f"https://api.genius.com/search?q={song_title} {artist_name}"
    headers = {'Authorization': 'Bearer YOUR_ACCESS_TOKEN'}  # Replace with your Genius API token
    response = requests.get(search_url, headers=headers)
    data = response.json()
    
    if data['response']['hits']:
        song_path = data['response']['hits'][0]['result']['path']
        lyrics_url = f"https://genius.com{song_path}"
        
        # Scraping lyrics from the Genius page
        page = requests.get(lyrics_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        lyrics = soup.find("div", class_="lyrics").get_text()
        
        lyrics_text.delete("1.0", tk.END)
        lyrics_text.insert(tk.END, lyrics)
    else:
        lyrics_text.delete("1.0", tk.END)
        lyrics_text.insert(tk.END, "Lyrics not found.")

# Set up the main window
root = tk.Tk()
root.title("Lyrics Finder")

# Create input fields
tk.Label(root, text="Song Title:").grid(row=0, column=0, padx=10, pady=10)
title_entry = tk.Entry(root, width=50)
title_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Artist Name:").grid(row=1, column=0, padx=10, pady=10)
artist_entry = tk.Entry(root, width=50)
artist_entry.grid(row=1, column=1, padx=10, pady=10)

# Create a button to fetch lyrics
fetch_button = tk.Button(root, text="Fetch Lyrics", command=fetch_lyrics)
fetch_button.grid(row=2, column=0, columnspan=2, pady=10)

# Create a text area to display lyrics
lyrics_text = tk.Text(root, wrap=tk.WORD, width=60, height=20)
lyrics_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Run the application
root.mainloop()
