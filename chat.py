from tkinter import * 
import customtkinter
import openai
import os
import pickle 

# Intitiate App
root = customtkinter.CTk() # create custom kinter instance
root.title("ChatGPT Bot")
root.geometry('600x600')
root.iconbitmap('ai_lt.ico')

# Set Color Scheme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Submit to ChatGPT
def speak():
	if chat_entry.get():
		# Define our filename
		filename = "api_key"

		try:
			if os.path.isfile(filename):
				# Open the file
				input_file = open(filename, 'rb') # rb allows the file to be read

				# Load the data from the file into stuff variable
				stuff = pickle.load(input_file)

				# Query ChatGPT
				# Define our API Key to ChatGPT
				openai.api_key = stuff

				# Create instance
				openai.Model.list()

				# Define our Query/Response (for detailed info on each of these components, visit openai documentation)
				response = openai.Completion.create(
					model = "text-davinci-003", # multiple models available, this is just one of them
					prompt = chat_entry.get(),
					temperature = 0, # 0 is default, if you want more specific data, you would raise the temperature to 1, 2, etc
					max_tokens = 60, # text that is returned
					top_p = 1.0,
					frequency_penalty = 0.0,
					presence_penalty = 0.0,
					)

				my_text.insert(END, (response["choices"][0]["text"]).strip()) # parse the data, get first item in choices list
				my_text.insert(END, "\n\n") 
			else:
				# Create the file
				input_file = open(filename, 'wb') # wb allows write to file
				# Close the file
				input_file.close()
				# Error Message
				my_text.insert(END, "\n\nYou Need an API Key to Talk with ChatGPT. Get One here: \nhttps://platform.openai.com/account/api-keys")

		except Exception as e:
			my_text.insert(END, f"\n\n There was an error\n\n{e}")
	else:
		my_text.insert(END, "\n\nText entry is empty, please enter some text.")

# Clear the Screens
def clear():
	# Clear the Main Text Box, text boxes start at 1 not 0
	my_text.delete(1.0, END) # first position in textbox (top left corner) to end of box
	# Clear the qyery entry widget
	chat_entry.delete(0, END)


# Do API stuff
def key():
	# Define our filename
	filename = "api_key"

	try:
		if os.path.isfile(filename):
			# Open the file
			input_file = open(filename, 'rb') # rb allows the file to be read

			# Load the data from the file into stuff variable
			stuff = pickle.load(input_file)

			# Output to stuff to our entry box
			api_entry.insert(END, stuff)
		else:
			# Create the file
			input_file = open(filename, 'wb') # wb allows write to file
			# Close the file
			input_file.close()

	except Exception as e:
		my_text.insert(END, f"\n\n There was an error\n\n{e}")

	# Resize App Larger
	root.geometry('600x750')
	# Reshow API Frame
	api_frame.pack(pady=30)


# Save the API Key
def save_key():
	# Define our filename
	filename = "api_key"

	try:
		# Open the file
		output_file = open(filename, 'wb')

		# Add the data to the file
		pickle.dump(api_entry.get(), output_file) # get text from api_entry box

		# Delete Entry box
		api_entry.delete(0, END) 

		# Hide API Frame
		api_frame.pack_forget() 
		# Rsize App Smaller
		root.geometry('600x600') 

	except Exception as e:
		my_text.insert(END, f"\n\n There was an error\n\n{e}")

# Create Text Frame
text_frame = customtkinter.CTkFrame(root)
text_frame.pack(pady=20) # display to screen

# Add Text Widget to Get ChatGPT Responses
my_text = Text(text_frame, # add to text frame
	bg="#343638", # add background color
	width=65, # set width
	bd=1, # set border
	fg="#d6d6d6", # add foreground color
	relief="flat", # removes white line around border
	wrap=WORD, # word wrap
	selectbackground="#1f538d" # changes highlighted text color
	) 
my_text.grid(row=0, column=0) # grid will be inside of text frame

# Create scrollbar for text widget
text_scroll = customtkinter.CTkScrollbar(text_frame,
	command=my_text.yview)
text_scroll.grid(row=0, column=1, sticky='ns') # apply ns sticky so scrollbar extends the entire length of the widget

# Add the scrollbar to teh textbox
my_text.configure(yscrollcommand=text_scroll.set)


# Entry Widget to enter text to send to ChatGPT
chat_entry = customtkinter.CTkEntry(root,
	placeholder_text="Type Something To ChatGPT...",
	width=535,
	height=50,
	border_width=1)
chat_entry.pack(pady=10)

# Create Button Frame
button_frame = customtkinter.CTkFrame(root, fg_color="#242424")
button_frame.pack(pady=10)

# Create Submit Button
submit_button = customtkinter.CTkButton(button_frame,
	text="Speak to ChatGPT",
	command=speak)
submit_button.grid(row=1, column=0, padx=25)


# Create Clear Button
clear_button = customtkinter.CTkButton(button_frame,
	text="Clear Response",
	command=clear)
clear_button.grid(row=1, column=1, padx=35)

# Create API Button
api_button = customtkinter.CTkButton(button_frame,
	text="Update API Key",
	command=key)
api_button.grid(row=1, column=2, padx=25)


# Add API Key Frame
api_frame = customtkinter.CTkFrame(root, border_width=1)
api_frame.pack(pady=30)

# Add API Entry Widget
api_entry = customtkinter.CTkEntry(api_frame,
	placeholder_text="Enter your API Key",
	width=350,
	height=50,
	border_width=1)
api_entry.grid(row=0, column=0, padx=20, pady=20)

# Add API Button
api_save_button = customtkinter.CTkButton(api_frame, 
	text="Save Key",
	command=save_key)
api_save_button.grid(row=0, column=1, padx=10)

root.mainloop()