#code to operate a Raspberry-Pi Based DALEK Robot

from typing import Union


#provides the actual command line interface used by the input and output comms
class CommandLineInterface():
    #initialises the command line
    def __init__(self):
        pass
    
    #print the text of a message
    def print_message(self,message : str) -> None:
        print(message)
    
    #get text input
    #research non-blocking input later
    #https://stackoverflow.com/questions/2408560/non-blocking-console-input
    def get_input(self,input_message : str) -> str:
        user_input : str = input(input_message)
        return user_input

#handles communication from the user to the DALEK
class InputComms():
    #initalises the input comm system
    def __init__(self,text_active : bool = True,voice_active : bool = False,gui_active : bool = False) -> None:
        self.text_active : bool = text_active #have we enabled command line text input
        self.voice_active : bool = voice_active #have we enabled voice input
        self.gui_active   : bool = gui_active #have we enabled gui input
        self.command_line_exists : bool = False

    #add the command line to the input comms
    def add_command_line(self,command_line_interface):
        self.command_line_exists = True
        self.command_line : CommandLineInterface = command_line_interface

    #get user input from the command line
    def get_user_input_command_line(self,input_message : str) -> tuple[bool,str]:
        error : bool = False
        message : str = 'undefined'
        if self.command_line == None:
            error = True
            message = "ERROR : NO COMMAND LINE OUTPUT"
        else:
            message = self.command_line.get_input(input_message)

        return error,message
    
    #get user input
    def get_user_input(self,input_message : str,use_text : bool = True, use_voice : bool = False) -> str: 
        #at the moment, this is just a wrapper for get_user_input_command_line
        error : bool = False
        message : bool = "Undefined"
        if self.text_active and use_text: #if we are using text input
            error,message = self.get_user_input_command_line(input_message)
        #add error handling here
        return message



#handles communication from the DALEK to the user
class OutputComms():
    #initalises the output comm system
    def __init__(self,text_active : bool = True,voice_active : bool = False,text_debug : bool = False,voice_debug : bool = False,gui_active : bool = False) -> None:
        #set flags for if various features are active
        self.text_active : bool = text_active #have we enabled command line text output
        self.voice_active : bool = voice_active #have we enabled voice output
        self.text_debug : bool = text_debug #are we printing debug messages
        self.voice_debug : bool = voice_debug #are we using voice output for debug messages
        self.gui_active   : bool = gui_active #have we activated the GUI
        self.command_line_exists : bool = False #the command line interface does not exist by default

    #add the command line to the output comms
    def add_command_line(self,command_line_interface) -> None:
        self.command_line_exists = True
        self.command_line : CommandLineInterface = command_line_interface
    
    #pass a message to the user through the command line
    def broadcast_command_line(self,message : str) -> None:
        if self.command_line == None:
            pass #do nothing, we have no command line to broadcast too
        else:
            self.command_line.print_message(message)

    #pass a message to the user through voice output
    def broadcast_voice(self,message : str) ->None:
        pass #do nothing for now, we not yet developed this code

    #pass a message to the user, use_text and use_voice determine if we use text and voice channels if those are active
    #default is to use both if possible
    def message_user(self,message : str,use_text : bool = True,use_voice : bool = True):
        if self.text_active and use_text: #if text is available and we are using it
            self.broadcast_command_line(message)
        if self.voice_active and use_voice:
            self.broadcast_voice(message)



#responsible for overall communication between the Dalek and the User
#it recieves user messages, processes them and then uses the correct commands on the DalekOS class.
class UserCommsManager():
    #initalise the manager
    def __init__(self):
        self.setup_command_line()
        self.setup_input_comms()
        self.setup_output_comms()
    #add a reference to the master of this manager so we can communicate back to the master
    def add_master(self,master : 'DalekOS'):
        self.master = master

    def setup_command_line(self):
        self.command_line = CommandLineInterface()

    #setup the input comms system
    def setup_input_comms(self):
        self.input_comms = InputComms() #create the object
        self.input_comms.add_command_line(self.command_line) #provide it with access to the command line

    #setup the output comms system
    def setup_output_comms(self):
        self.output_comms = OutputComms() #create the object
        self.output_comms.add_command_line(self.command_line) #provide it with access to the command line

    #run the communication module
    def run(self):
        while True:
            self.output_comms.message_user("I AM DALEK, WHAT IS YOUR COMMAND")
            user_message = self.input_comms.get_user_input("PLEASE STATE COMMAND : ")
            self.output_comms.message_user("RECIEVED COMMAND " + user_message + " I OBEY")


#the highest level class, responsible for overall control of the DALEK
class DalekOS:
    #initalise the operating system
    def __init__(self):
        self.setup_comms_manager() #setup and start the comms manager (needs to be done last or code will block)
    
    #setup and start the comms manager
    def setup_comms_manager(self) -> None:
        self.user_comms_manager : UserCommsManager = UserCommsManager() #create the comms manager
        self.user_comms_manager.add_master(self) #inform them who you are
        self.user_comms_manager.run() #run the comms manager, this needs to be done last
    

#main function, sets up the DALEK
def main():
    Dalek = DalekOS()


if __name__ == "__main__":
    main()