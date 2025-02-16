import re


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
    

class Santa(metaclass=Singleton):
    _MAX_AGE = 5

    def __init__(self):
        self._wishes = {}

    def _get_wish(self, text):
        """Get the wish from the letter/call"""
        
        pattern = r'[\"\']([A-Za-z0-9 ]+)[\"\']'
        wish = re.search(pattern, text)
        if wish:
            return wish.group(1)

    def __call__(self, kid, text):
        wish = self._get_wish(text)
        if wish:
           self._wishes[id(kid)] = wish  
                
    def _get_signature(self, text):
        """Get the signature of the kid from the letter"""

        pattern = r'\b\d+\b(?=\s*$)'
        signature = re.search(pattern, text)
        if signature:
            return signature.group().strip()
    
    def __matmul__(self, text):
        signature = self._get_signature(text)
        wish = self._get_wish(text)
        if signature and wish:
           self._wishes[int(signature)] = wish  

    def __iter__(self):
        for val in self._wishes.values():
            yield val
    
    @property
    def _get_most_wanted_gift(self):
        """Get the most wanted gift"""

        wishes = list(self._wishes.values())
        return max(wishes, key=wishes.count)
    
    def _clear_xmas(self):
        """Clear the wishes and _naughty_kids"""

        self._wishes.clear()
        Kid._naughty_kids.clear()

    def xmas(self):
        Kid._increment_ages()

        if not self._wishes:
            return
        
        most_wanted_gift = self._get_most_wanted_gift
        for identity, kid in Kid._kids_instances.items():
            if Kid._kids_ages[identity] <= self._MAX_AGE:
                if kid in Kid._naughty_kids:
                    kid('coal')
                else:
                    if identity in self._wishes:
                        wish = self._wishes[identity]
                    else:
                        wish = most_wanted_gift
                    kid(wish)

        self._clear_xmas()
        

class Kid(type):
    _kids_ages = {}
    _kids_instances = {}
    _naughty_kids = set()
    
    @classmethod
    def _check_naughty(cls, method):
        def wrapper(self, *args, **kwargs):
            """Add the instance to _naughty_kids if an exception is raised in method"""

            try:
                return method(self, *args, **kwargs)
            except Exception:
                cls._naughty_kids.add(self)
                raise
        return wrapper

    def __new__(cls, name, bases, dct):
        if '__call__' not in dct:
            raise NotImplementedError('Sorry, but the instance of the class should be callable (dont get angry, please) :)')
        
        for attribute_name, attribute_val in dct.items():
            if callable(attribute_val):
                if not attribute_name.startswith('_'):
                    dct[attribute_name] = cls._check_naughty(attribute_val)

        return super().__new__(cls, name, bases, dct)
    
    def __call__(cls, *args, **kwargs):      
        new_kid = super().__call__(*args, **kwargs)
        identity = id(new_kid)
        cls._kids_ages[identity] = 0
        cls._kids_instances[identity] = new_kid
        return new_kid
        
    @classmethod
    def _increment_ages(cls):
        """Increment the age of each kid by one year"""

        for identity, age in cls._kids_ages.items():
            cls._kids_ages[identity] += 1 

        
    

    
    
    
    
    
    
    
    
    
    
    santa = Santa()



class BulgarianKid(metaclass=Kid):

    def __call__(self, present):
        print(f"BulgarianKid получи подарък: {present}")

    def be_naughty(self):
        raise RuntimeError('Няма да си изям зеленчуците!')


class ChineseKid(metaclass=Kid):

    def __call__(self, present):
        print(f"ChineseKid получи подарък: {present}")


goshko = BulgarianKid()
toshko = BulgarianKid()
chen = ChineseKid()

santa = Santa()

santa(goshko, "'gun'")
santa @ f"'gun'\n{id(toshko)}"

try:
    goshko.be_naughty()
except:
    pass

santa.xmas()
# Гошко получава coal
# Тошко получава gun
# Chen получава gun

santa.xmas()
# Никой не получава нищо, защото няма желания

santa.xmas()
# Никой не получава нищо, защото няма желания

santa.xmas()
# Никой не получава нищо, защото няма желания

gencho = BulgarianKid()
santa(gencho, "'whistle'")

santa.xmas()
# Всички деца (Гошко, Тошко, Cheng и Генчо) получават whistle

kircho = BulgarianKid()
santa(kircho, "'whistle'")

santa.xmas()
# Кирчо и Генчо получават whistle. Останалите вече са на над 5 години.