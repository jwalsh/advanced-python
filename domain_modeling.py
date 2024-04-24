# Domain Modeling with Classes Exercise

# In this exercise, you'll be modeling the domain of a pet store based on the Swagger Petstore API.
# The pet store has the following entities:
# - Pet: Represents a pet in the store. Each pet has an ID, name, status, category, and tags.
# - Category: Represents a category of pets. Each category has an ID and name.
# - Tag: Represents a tag associated with a pet. Each tag has an ID and name.

# The relationships between the entities are as follows:
# - A pet belongs to one category.
# - A pet can have multiple tags.
# - A tag can be associated with multiple pets.

# Your task is to create the necessary classes to model this domain and establish the relationships between them.

# Step 1: Create the Category class
# - The Category class should have an `id` attribute (integer) and a `name` attribute (string).
# - Implement an `__init__` method to initialize the `id` and `name` attributes.
# - Implement a `__repr__` method to provide a string representation of the Category object.

# Step 2: Create the Tag class
# - The Tag class should have an `id` attribute (integer) and a `name` attribute (string).
# - Implement an `__init__` method to initialize the `id` and `name` attributes.
# - Implement a `__repr__` method to provide a string representation of the Tag object.

# Step 3: Create the Pet class
# - The Pet class should have the following attributes:
#   - `id` (integer): The unique identifier of the pet.
#   - `name` (string): The name of the pet.
#   - `status` (string): The status of the pet (e.g., "available", "pending", "sold").
#   - `category` (Category): The category the pet belongs to.
#   - `tags` (list of Tag objects): The tags associated with the pet.
# - Implement an `__init__` method to initialize the attributes of the Pet class.
# - Implement a `__repr__` method to provide a string representation of the Pet object.
# - Implement an `add_tag` method that allows adding a Tag object to the `tags` list.

# Step 4: Create sample objects and establish relationships
# - Create a few sample Category objects.
# - Create a few sample Tag objects.
# - Create a few sample Pet objects, associating them with categories and tags.

# Step 5: Test the relationships
# - Print the string representation of each Pet object, including its category and tags.
# - Verify that the relationships between pets, categories, and tags are properly established.

# Step 6: Refactor the Pet.status attribute to use an Enum
# - Refactor the `status` attribute of the Pet class to use an Enum for the possible pet statuses ("available", "pending", "sold").
# - Update the Pet class to use the Enum for the `status` attribute.
# - Update the sample Pet objects to use the Enum for the `status` attribute.

# Example usage:
# category1 = Category(1, "Dogs")
# category2 = Category(2, "Cats")
#
# tag1 = Tag(1, "Fluffy")
# tag2 = Tag(2, "Playful")
#
# pet1 = Pet(1, "Buddy", "available", category1)
# pet1.add_tag(tag1)
# pet1.add_tag(tag2)
#
# pet2 = Pet(2, "Whiskers", "pending", category2)
# pet2.add_tag(tag1)
#
# print(pet1)
# print(pet2)

# Expected output:
# Pet(id=1, name='Buddy', status='available', category=Category(id=1, name='Dogs'), tags=[Tag(id=1, name='Fluffy'), Tag(id=2, name='Playful')])
# Pet(id=2, name='Whiskers', status='pending', category=Category(id=2, name='Cats'), tags=[Tag(id=1, name='Fluffy')])
