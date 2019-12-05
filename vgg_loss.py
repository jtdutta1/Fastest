import argparse
import numpy as np
from tensorflow.keras.layers import Conv2D, LeakyReLU, AveragePooling2D, UpSampling2D, concatenate, Input
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.losses import MeanSquaredError

vgg_model = None

'''
You need the vgg model for this. I will provide the link here.
https://drive.google.com/open?id=1OsKx6CPacs7V7d-1cNCI2bFIty2BVQEz
'''


def create_args():
    parser = argparse.ArgumentParser(prog='Some Model')
    parser.add_argument('-p', '--path', help='Path to VGG model')
    return parser.parse_args()


def unet(inputs, first_block_receptive_field=(3, 3), second_block_receptive_field=(3, 3), name="UNet"):
    def _down(inp, name, filters, kernel=(3, 3), strides=(1, 1), padding='same'):
        conv1 = Conv2D(filters, kernel_size=kernel, strides=strides, padding=padding, name=name + '_1')(inp)
        conv1 = LeakyReLU(alpha=0.1)(conv1)
        conv2 = Conv2D(filters, kernel_size=kernel, strides=strides, padding=padding, name=name + '_2')(conv1)
        conv2 = LeakyReLU(alpha=0.1)(conv2)
        return conv2

    def _up(inp, con, name, filters, kernel=(3, 3), strides=(1, 1), padding='same'):
        concat = concatenate([con, inp], axis=-1)
        conv1 = Conv2D(filters, kernel_size=kernel, strides=strides, padding=padding, name=name + '_1')(concat)
        conv1 = LeakyReLU(alpha=0.1)(conv1)
        conv2 = Conv2D(filters, kernel_size=kernel, strides=strides, padding=padding, name=name + '_2')(conv1)
        conv2 = LeakyReLU(alpha=0.1)(conv2)
        return conv2

    block1 = _down(inputs, name + '_' + 'conv1', filters=32, kernel=first_block_receptive_field)
    pool1 = AveragePooling2D(pool_size=(2, 2), strides=(2, 2))(block1)

    block2 = _down(pool1, name + '_' + 'conv2', filters=64, kernel=second_block_receptive_field)
    pool2 = AveragePooling2D(pool_size=(2, 2), strides=(2, 2))(block2)

    block3 = _down(pool2, name + '_' + 'conv3', filters=128, kernel=(3, 3))
    pool3 = AveragePooling2D(pool_size=(2, 2), strides=(2, 2))(block3)

    block4 = _down(pool3, name + '_' + 'conv4', filters=256, kernel=(3, 3))
    pool4 = AveragePooling2D(pool_size=(2, 2), strides=(2, 2))(block4)

    block5 = _down(pool4, name + '_' + 'conv5', filters=512, kernel=(3, 3))
    pool5 = AveragePooling2D(pool_size=(2, 2), strides=(2, 2))(block5)

    block6 = _down(pool5, name + '_' + 'conv6', filters=512, kernel=(3, 3))

    up1 = UpSampling2D(size=(2, 2), interpolation='bilinear')(block6)
    block7 = _up(up1, block5, name=name + '_' + 'conv7', filters=512)

    up2 = UpSampling2D(size=(2, 2), interpolation='bilinear')(block7)
    block8 = _up(up2, block4, name=name + '_' + 'conv8', filters=256)

    up3 = UpSampling2D(size=(2, 2), interpolation='bilinear')(block8)
    block9 = _up(up3, block3, name=name + '_' + 'conv9', filters=128)

    up4 = UpSampling2D(size=(2, 2), interpolation='bilinear')(block9)
    block10 = _up(up4, block2, name=name + '_' + 'conv10', filters=64)

    up5 = UpSampling2D(size=(2, 2), interpolation='bilinear')(block10)
    block11 = _up(up5, block1, name=name + '_' + 'conv11', filters=32)

    return block6, block11
    # return block11


def some_model(inputs):
    _, out = unet(inputs)
    out = Conv2D(filters=3,
                 kernel_size=(3, 3),
                 padding='same',
                 activation=LeakyReLU(alpha=0.1),
                 name='PostProcess')(out)
    return out


def some_loss(y_true, y_pred):
    mse = MeanSquaredError()
    global vgg_model
    return mse(vgg_model.predict(y_pred, steps=1), vgg_model.predict(y_true, steps=1))


def main():
    parser = create_args()
    global vgg_model
    vgg_model = load_model(parser.path)
    inputs = Input(shape=[512, 512, 3], batch_size=1, name='input_node')
    out = some_model(inputs)
    model = Model(inputs=inputs, outputs=out)
    model.summary()
    model.compile(optimizer='adam', loss=some_loss, metrics=['accuracy'])
    X = np.random.randn(1, 512, 512, 3)
    Y = np.random.randn(1, 512, 512, 3)
    model.fit(X, Y, epochs=1, batch_size=1)


main()
