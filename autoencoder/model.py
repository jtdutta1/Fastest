from torch import nn

class Encoder(nn.Module):
    """
    Encoder for dimensional reduction.
    
    """
    
    def __init__(self, input_size=784, nlayers=5, output_size=10):
        super(Encoder, self).__init__()
        # Check whether dimensional reduction to 
        # the last hidden layer is more than the output_size
        assert input_size/(2**nlayers) >= output_size
        self.layer_dims = [(input_size//(2**i), input_size//(2**(i+1))) for i in range(nlayers)]
        self.hidden = nn.Sequential(*[nn.Linear(in_features=i[0], out_features=i[1]) for i in self.layer_dims])
        self.output = nn.Linear(in_features=self.layer_dims[-1][-1], out_features=output_size)
        self.output_size=output_size
    
    def forward(self, x):
        x = self.hidden(x)
        x = self.output(x)
        return x
    
class Decoder(nn.Module):
    """
    Decoder for dimensional reduction.
    
    """
    
    def __init__(self, input_size=10, nlayers=5, output_size=784):
        super(Decoder, self).__init__()
        # Check whether dimensional reduction to 
        # the last hidden layer is more than the output_size
        assert output_size/(2**nlayers) >= input_size
        self.layer_dims = [(output_size//(2**i), output_size//(2**(i+1))) for i in range(nlayers)]
        self.layer_dims.reverse()
        self.layer1 = nn.Linear(in_features=input_size, out_features=self.layer_dims[0][1])
        self.hidden = nn.Sequential(*[nn.Linear(in_features=i[1], out_features=i[0]) for i in self.layer_dims])
    
    def forward(self, x):
        x = self.layer1(x)
        x = self.hidden(x)
        return x


class EncoderDecoder(nn.Module):
    """
    Encoder Decoder architecture for recreating mnist digits using dimensional reduction
    
    """
    
    def __init__(self, input_size=784, output_size=784, enc_layers=5, dec_layers=5):
        super(EncoderDecoder, self).__init__()
        self.encoder = Encoder(input_size, 
                               nlayers=enc_layers)
        self.decoder = Decoder(input_size=self.encoder.output_size,
                               nlayers=dec_layers)
    
    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x