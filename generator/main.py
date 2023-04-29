from generator import Generator

generator = Generator(length=200, code=Generator.ALL, format=Generator.JSON)
generator.generate()
print('Saved.' if generator.save() else 'Not saved.')