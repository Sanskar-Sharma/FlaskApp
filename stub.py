# GET	/store/{id}/tag	Get a list of tags in a store.
# POST	/store/{id}/tag	Create a new tag.
# POST	/item/{id}/tag/{id}	Link an item in a store with a tag from the same store.
# DELETE	/item/{id}/tag/{id}	Unlink a tag from an item.
# GET	/tag/{id}	Get information about a tag given its unique id.
# DELETE	/tag/{id}	Delete a tag, which must have no associated items.