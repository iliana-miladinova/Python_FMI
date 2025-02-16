class Material:
    DENSITY = 0

    def __init__(self, mass):
        self.mass = mass

    @property
    def volume(self):
        return float(self.mass / self.DENSITY)
    

class Concrete(Material):
    DENSITY = 2500


class Brick(Material):
    DENSITY = 2000


class Stone(Material):
    DENSITY = 1600


class Wood(Material):
    DENSITY = 600


class Steel(Material):
    DENSITY = 7700


class Factory:
    _MATERIALS = { 
        'Concrete': Concrete,
        'Brick': Brick,
        'Stone': Stone,
        'Wood': Wood,
        'Steel': Steel
        }
    
    _alloys = {}
    _all_materials = set()
    _used_materials = set()
   
    def __init__(self):
        self._curr_materials = set()

    def __call__(self, *args, **kwargs):
        if args and kwargs:
            raise ValueError('Function can be called with only positional or only keyword arguments')
        elif not args and not kwargs:
            raise ValueError('Function cannot be called without arguments')
        elif kwargs:
            return self._get_result_from_kwargs(**kwargs) 
        elif args:
            return self._get_alloy_from_args(*args)
                
    def _get_result_from_kwargs(self, **kwargs):
        """Return tuple of instances of materials, created from keyword arguments."""  
        res = []
        for key, val in kwargs.items():
            material = self._MATERIALS.get(key)
            if material is None:
                material = Factory._alloys.get(key)
                
            if material is None or not issubclass(material, Material):
                raise ValueError('Invalid material')
            
            new_material = material(val)
            Factory._all_materials.add(new_material) 
            self._curr_materials.add(new_material)
            
            res.append(new_material)

        return tuple(res)
    
    def _get_average_density(self, *args):
        """Return the average density of the materials."""
        density_sum = 0
        for arg in args:
            density_sum += type(arg).DENSITY
        
        average_density = density_sum / len(args)
        return average_density
    
    def _get_mass(self, *args):
        """Calculate the sum of the masses of the materials"""
        mass_sum = 0
        for arg in args:
            mass_sum += arg.mass

        return mass_sum

    def _get_alloy_from_args(self, *args):
        """Create a dynamic class (alloy) from materials."""
        base_classes_names = []

        for arg in args:
            if arg in Factory._used_materials:
                raise AssertionError('Invalid material')
            
            Factory._used_materials.add(arg)
            
            base_classes_names.extend(type(arg).__name__.split('_'))
            
        sorted_materials_names = sorted(base_classes_names)
        new_alloy_name = '_'.join(sorted_materials_names)

        if new_alloy_name not in Factory._alloys:
            average_density = self._get_average_density(*args)
            alloy = type(
                new_alloy_name,
                  (Material,), 
                  {'DENSITY': average_density}
                )
            Factory._alloys[new_alloy_name] = alloy

        alloy = Factory._alloys[new_alloy_name]
        alloy_mass = self._get_mass(*args)
        
        new_alloy = alloy(alloy_mass)
        self._curr_materials.add(new_alloy)
        Factory._all_materials.add(new_alloy)
        return new_alloy
        
    def can_build(self, needed_volume):
        volume_sum = 0
        for material in self._curr_materials:
            if material not in Factory._used_materials:
                volume_sum += material.volume
        
        return volume_sum >= needed_volume
    
    @classmethod
    def can_build_together(cls, needed_volume):
        volume_sum = 0
        for material in cls._all_materials:
            volume_sum += material.volume

        return volume_sum >= needed_volume