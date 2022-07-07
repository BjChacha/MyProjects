import numpy as np
import matplotlib.pyplot as plt
import imageio
import time
import os
import shutil

# Params
# 图像大小
H = 160
W = 240

# 稀疏度
sparse = 0.05

# gif时长，单位为second
gif_duration = 10

# gif帧率
gif_fps = 12

temps_folder = 'temps'

def next_frame(image):
    neibor = collect_neibor(image)
    birth = (neibor == 3) & (image == 0)
    survive = ((neibor == 2) | (neibor == 3)) & (image == 1)
    image[...] = 0
    image[birth | survive] = 1


def collect_neibor(image):
    image_padding = np.pad(image, ((1, 1), (1, 1)),
                           'constant', constant_values=0)
    res = (image_padding[0:-2, 0:-2] + image_padding[0:-2, 1:-1] + image_padding[0:-2, 2:] +
           image_padding[1:-1, 0:-2] + image_padding[1:-1, 2:] +
           image_padding[2:, 0:-2] + image_padding[2:, 1:-1] + image_padding[2:, 2:])
    return res


def main():
    # 随机矩阵
    game = np.zeros((H, W))
    for i in range(int(H*W*sparse)):
        x, y = np.random.randint(H), np.random.randint(W)
        if game[x, y] == 0:
            game[x, y] = 1

    # 固定模式
    # game = np.zeros((17, 17))
    # pattern 1
    # game[4, 3:6] = 1
    # pattern 2
    # game[1, 1] = 1
    # game[2, 1:3] = 1
    # pattern 3
    # game[1, 2] = game[2, 3] = game[3, 1:4] = 1
    # # pattern 4
    # game = np.zeros((39, 39))
    # game[37, 4:6] = game[37, 13:15] = game[37, 24:26] = game[37,33:35] = 1
    # game[36, 16] = game[36, 22] = 1
    # game[35, 4] = game[35, 9] = game[35, 13] = game[35, 18] = 1
    # game[35, 20] = game[35, 25] = game[35, 29] = game[35,34] = 1
    # game[34, 5:7] = game[34, 8] = game[34,13] = game[34,15:17] = game[34,18:21] = 1
    # game[34, 22:24] = game[34, 25] = game[34, 30] = game[34, 32:34] = 1
    # game[33, 6] = game[33, 8] = game[33, 10:12] = game[33, 13:15] = game[33, 18:21] = 1
    # game[33,24:26] = game[33, 27:29] = game[33, 30] = game[33, 32] = 1
    # game[32, 7:9] = game[32, 13] = game[32, 25] = game[32, 30:32] = 1
    # game[31, 8] = game[31, 12] = game[31,26] = game[31,30] = 1
    # game[30, 9:12] = game[30,27:30] = 1

    # # 创造模式
    # game = [[0, 0, 0, 0, 0, 0, 1, 0],
    #                 [0, 0, 0, 0, 1, 0, 1, 1],
    #                 [0, 0, 0, 0, 1, 0, 1, 0],
    #                 [0, 0, 0, 0, 1, 0, 0, 0],
    #                 [0, 0, 1, 0, 0, 0, 0, 0],
    #                 [1, 0, 1, 0, 0, 0, 0, 0]]
    # game = np.array(game)
    # game = np.pad(game, ((5, 5), (5, 5)), 'constant', constant_values=0)

    # frames = []
    if os.path.exists(temps_folder):
        shutil.rmtree(temps_folder)
    os.makedirs(temps_folder)

    for i in range(int(gif_duration * gif_fps)):
        # plt.imshow(game)
        # plt.pause(delay)
        # frames.append(game.copy())

        fig = plt.figure()
        plt.axis('off')
        plt.xticks([])
        plt.yticks([])
        plt.imshow(game.copy())
        fig.savefig("temps/{}.png".format(i+1))
        plt.close()

        next_frame(game)

    write_gif(
        '{}_GoL_{}x{}_{}_{}x{}.gif'.format(time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time())), W, H, sparse, gif_duration, gif_fps),
        temps_folder,
        gif_fps,
        )
    # with imageio.get_writer('{}_GoL_{}x{}_{}_{}x{}.gif'.format(time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time())), W, H, sparse, gif_duration, gif_fps), mode='I') as writer:
    #     img_list = os.listdir(temps_folder)
    #     img_list.sort(key = lambda x: int(x[:-4]))
    #     for fname in img_list:
    #         image = imageio.imread(os.path.join(temps_folder, fname))
    #         writer.append_data(image)

    shutil.rmtree(temps_folder)

    # frames.append(game.copy())



def write_gif(save_path, temp_path, fps):
    img_list = os.listdir(temp_path)
    img_list.sort(key = lambda x: int(x[:-4]))
    frames = []
    for fname in img_list:
        frames.append(imageio.imread(os.path.join(temps_folder, fname)))

    imageio.mimsave(save_path, frames, fps=fps)


def debug():
    fig = plt.figure()
    plt.axis('off')
    plt.xticks([])
    image = np.zeros((5, 5))
    image[1, 2] = image[2, 3] = image[3, 1:4] = 1
    plt.imshow(image)
    plt.imsave('test.png', image, dpi=1500)
    plt.show()


if __name__ == "__main__":
    main()
    # debug()
