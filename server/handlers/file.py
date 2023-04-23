def file_search(user_input):
    print(user_input)
    results = [
        {
            "name": "book.pdf",
            "clients": ["123.456.789", "321.654.978", "132.465.798"],
            "size": 65535,
            "blocks": 42,
            "checksum": "asdfqwerzxcv"
        },
        {
            "name": "vulture.mp4",
            "clients": ["123.456.789"],
            "size": 123456,
            "blocks": 33,
            "checksum": "asdfghjkl"
        },
        {
            "name": "happiness.png",
            "clients": ["127.0.0.1"],
            "size": 1,
            "blocks": 1,
            "checksum": "stoolandrope"
        },
    ]
    return results
