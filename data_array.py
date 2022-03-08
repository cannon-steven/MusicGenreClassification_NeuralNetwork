# This file will contain the init data array that will be
# used for the application init state.
# Every time a user adds a song, data will be appended to it which will
# temporarily live in the user's session.
cnn_data_array = [
            {
                "filename": "blues.wav",
                "genre": {
                    "blues": 61, "classical": 5, "country": 5,
                    "disco": 4, "hiphop": 5, "jazz": 5, "metal": 5,
                    "pop": 5, "reggae": 5, "rock": 5
                }
            },
            {
                "filename": "bad.wav",
                "genre": {
                    "blues": 60, "classical": 5, "country": 5,
                    "disco": 5, "hiphop": 5, "jazz": 5, "metal": 5,
                    "pop": 5, "reggae": 5, "rock": 5
                }
            },
            {
                "filename": "thriller.wav",
                "genre": {
                    "blues": 65, "classical": 5, "country": 5,
                    "disco": 0, "hiphop": 5, "jazz": 5, "metal": 5,
                    "pop": 5, "reggae": 5, "rock": 5
                }
            },
            {
                "filename": "hello.wav",
                "genre": {
                    "blues": 10, "classical": 5, "country": 5,
                    "disco": 0, "hiphop": 5, "jazz": 5, "metal": 5,
                    "pop": 60, "reggae": 5, "rock": 5
                }
            }
        ]


def make_genres_dict(cnn_data):
    genres = [
        "Blues", "Classical", "Country", "Disco",
        "Hiphop", "Jazz", "Metal", "Pop", "Reggae", "Rock"
    ]
    data_object = {genres[i]: cnn_data[i] for i in range(len(genres))}
    return data_object


def check_for_duplicates(data_array, new_file):
    for i in data_array:
        print(new_file in i['filename'])
        return new_file in i['filename']
