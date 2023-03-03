import json
import os
from datetime import datetime

from .AudioSystem import AudioSystem
from .NaturalLanguageProcessing import NaturalLanguageProcessing


class Command:
    """
        Dedicated class to process commands of assistant
    """
    natura_lang = NaturalLanguageProcessing()
    commands = {}
    audio = AudioSystem()
    
    
    def __init__(self) -> None:
        abspath = os.path.abspath("src/files/commands_synonyms.json")
        
        with open(abspath, encoding='utf-8') as commands_file:
            parsed_json = json.load(commands_file)
            self.commands = parsed_json
            
    def find_command(self, keywords: list[str]) -> str:
        """
            Method to find a internal command
        """
        for keyword in keywords:
            for key in self.commands:
                if keyword in self.commands[key]:
                    return key
        
        return ''
    
    def try_find_command_by_synonyms(self,  keywords: list[str]) -> str:
        """
            Method to try to find internal command using synonyms of keywords
        """
        for keyword in keywords:
            synonyms = self.natura_lang.get_synonyms(keyword)
                
            internal_command = self.find_command(synonyms)
                
            if internal_command != '':
                return internal_command
        
        return ''
    
    def run_command(self, command_key: str) -> bool:
        """
            Method to run command
        """
        
        match command_key:
            case "hora":
                now = datetime.now()
                hour = now.hour
                minutes = now.minute

                text = f'O horário atual é {hour} hora{hour > 1 and "s" or "" } e {minutes} minuto{minutes > 1 and "s" or "" }'
                self.audio.create_audio_by_text(text, 'command-output')
                self.audio.play_audio('command-output')
                print('comando hora executando')
        
    
    def process(self, command: str) -> bool:
        """
            Method to process and run command
        """
        
        print('')
        print("Comando: "+ command)
        print('')
        
        keywords = self.natura_lang.get_keywords(command)
        
        internal_command = self.find_command(keywords)
        
        print("internal_command: " + internal_command)
        
        # try to find internal command using synonyms of keywords
        if internal_command == '':
            internal_command = self.try_find_command_by_synonyms(keywords)
                        
        if internal_command != '':
            self.run_command(internal_command)
            return True
        

        
        return False