class HauntedMansion:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def __getattr__(self, name):
        return "Booooo, only ghosts here!"
    
    def __setattr__(self, name, val):
        
        super().__setattr__(f"spooky_{name}", val)

haunted_mansion = HauntedMansion(butler="Alfred", rooms=10, basement=True)
try:
    print(haunted_mansion.spooky_non_existent)
except AttributeError as e:
    print(e)
print(haunted_mansion.butler)
print(haunted_mansion.spooky_butler)
 
haunted_mansion.friendly_ghost = "Your favourite HP ghost - Nearly Headless Nick"
print(haunted_mansion.friendly_ghost)
 
print(haunted_mansion.spooky_friendly_ghost)
 
print(haunted_mansion.__class__)
print(haunted_mansion.__dict__)
try:
    print(haunted_mansion.spooky_something)
except AttributeError as e:
    print(e)
 
haunted_mansion._nikola_georgiev='Може ли да дадете пример за очаквано поведение при работа с protected атрибути'
print(haunted_mansion.spooky__nikola_georgiev)
print(haunted_mansion.__dict__)
haunted_mansion.spooky_smt="Iliana"
print(haunted_mansion.__dict__)