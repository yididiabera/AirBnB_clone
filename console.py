#!/usr/bin/python3

"""
Module for the entry point of the command interpreter.
This module defines the HBNBCommand class, which provides an interactive command-line
interface for interacting with the HBNB application.
"""

import cmd
from models.base_model import BaseModel
from models import storage
import re
import json


class HBNBCommand(cmd.Cmd):
    """
    Class for the command interpreter.
    This class inherits from `cmd.Cmd` and implements various commands to interact with
    the HBNB application, such as creating, showing, updating, and deleting instances.
    """

    prompt = "(hbnb) "
    # Uncomment the following line for a different prompt
    #prompt = "Type >> "

    def default(self, line):
        """
        Default handler for commands that are not explicitly defined.
        This method is called for any command that does not match a specific method
        and passes the command line to _precmd() for further processing.
        
        Args:
            line (str): The command line input.
        """
        # print("DEF:::", line)
        self._precmd(line)

    def _precmd(self, line):
        """
        Intercepts and processes commands to determine if they match the format
        class.method(arguments). If a match is found, the method is called with the
        provided arguments.
        
        Args:
            line (str): The command line input.
        
        Returns:
            str: The reformatted command if it matches the pattern; otherwise, returns the original line.
        """
        # print("PRECMD:::", line)
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not match:
            return line
        
        classname = match.group(1)
        method = match.group(2)
        args = match.group(3)
        
        match_uid_and_args = re.search(r'^"([^"]*)"(?:, (.*))?$', args)
        if match_uid_and_args:
            uid = match_uid_and_args.group(1)
            attr_or_dict = match_uid_and_args.group(2)
        else:
            uid = args
            attr_or_dict = None

        attr_and_value = ""
        if method == "update" and attr_or_dict:
            match_dict = re.search(r'^({.*})$', attr_or_dict)
            if match_dict:
                self.update_dict(classname, uid, match_dict.group(1))
                return ""
            match_attr_and_value = re.search(r'^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
            if match_attr_and_value:
                attr_and_value = (match_attr_and_value.group(1) or "") + " " + (match_attr_and_value.group(2) or "")
        
        command = f"{method} {classname} {uid} {attr_and_value}"
        self.onecmd(command)
        return command

    def update_dict(self, classname, uid, s_dict):
        """
        Updates an instance using a dictionary of attributes.

        Args:
            classname (str): The class name of the instance to update.
            uid (str): The unique identifier of the instance to update.
            s_dict (str): A JSON string representing the attributes to update.
        """
        s = s_dict.replace("'", '"')
        d = json.loads(s)
        
        if not classname:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = f"{classname}.{uid}"
            if key not in storage.all():
                print("** no instance found **")
            else:
                attributes = storage.attributes()[classname]
                for attribute, value in d.items():
                    if attribute in attributes:
                        value = attributes[attribute](value)
                    setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()

    def do_EOF(self, line):
        """
        Handles End Of File (EOF) character. Exits the program when EOF is encountered.
        
        Args:
            line (str): The command line input (not used in this method).

        Returns:
            bool: Always returns True to exit the command loop.
        """
        print()
        return True

    def do_quit(self, line):
        """
        Exits the program.
        
        Args:
            line (str): The command line input (not used in this method).

        Returns:
            bool: Always returns True to exit the command loop.
        """
        return True

    def emptyline(self):
        """
        Overrides the default behavior for an empty line. Does nothing on ENTER key press.
        """
        pass

    def do_create(self, line):
        """
        Creates a new instance of a class.

        Args:
            line (str): The class name of the instance to create.
        """
        if not line:
            print("** class name missing **")
        elif line not in storage.classes():
            print("** class doesn't exist **")
        else:
            b = storage.classes()[line]()
            b.save()
            print(b.id)

    def do_show(self, line):
        """
        Prints the string representation of an instance.

        Args:
            line (str): The class name and ID of the instance to display.
        """
        if not line:
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = f"{words[0]}.{words[1]}"
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name and ID.

        Args:
            line (str): The class name and ID of the instance to delete.
        """
        if not line:
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = f"{words[0]}.{words[1]}"
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_all(self, line):
        """
        Prints string representations of all instances, or all instances of a specific class.

        Args:
            line (str): The class name to filter by (empty string for all instances).
        """
        if line:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                nl = [str(obj) for key, obj in storage.all().items()
                      if type(obj).__name__ == words[0]]
                print(nl)
        else:
            new_list = [str(obj) for key, obj in storage.all().items()]
            print(new_list)

    def do_count(self, line):
        """
        Counts the number of instances of a specific class.

        Args:
            line (str): The class name to count instances of.
        """
        words = line.split(' ')
        if not words[0]:
            print("** class name missing **")
        elif words[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            matches = [k for k in storage.all() if k.startswith(words[0] + '.')]
            print(len(matches))

    def do_update(self, line):
        """
        Updates an instance by adding or modifying an attribute.

        Args:
            line (str): The class name, instance ID, attribute name, and value to update.
        """
        if not line:
            print("** class name missing **")
            return

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(rex, line)
        if not match:
            print("** class name missing **")
            return
        
        classname = match.group(1)
        uid = match.group(2)
        attribute = match.group(3)
        value = match.group(4)
        
        if classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = f"{classname}.{uid}"
            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                cast = None
                if not re.search(r'^".*"$', value):
                    if '.' in value:
                        cast = float
                    else:
                        cast = int
                else:
                    value = value.replace('"', '')
                attributes = storage.attributes()[classname]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:
                        pass  # Keep as string if casting fails
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
