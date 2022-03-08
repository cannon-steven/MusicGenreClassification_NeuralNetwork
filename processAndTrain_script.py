import AudioProcessing
import TrainModel

AudioProcessing.split_all("./genres_original", "./sliced_audio")
AudioProcessing.generate_spectrograms("./sliced_audio", "./Spectrograms")
TrainModel.train_model()
