import numpy as np
from numpy.testing import assert_allclose
import random
import math

from menpo.image import Image, MaskedImage
from menpo.feature import hog, lbp, es, igo
import menpo.io as mio


def test_imagewindowiterator_hog_padding():
    n_cases = 5
    image_width = np.random.randint(50, 250, [n_cases, 1])
    image_height = np.random.randint(50, 250, [n_cases, 1])
    window_step_horizontal = np.random.randint(1, 10, [n_cases, 1])
    window_step_vertical = np.random.randint(1, 10, [n_cases, 1])
    for i in range(n_cases):
        image = MaskedImage(np.random.randn(image_height[i, 0],
                                            image_width[i, 0], 1))
        hog_im = hog(image,
            mode='dense', window_step_vertical=window_step_vertical[i, 0],
            window_step_horizontal=window_step_horizontal[i, 0],
            window_step_unit='pixels', padding=True)
        n_windows_horizontal = len(range(0, image_width[i, 0],
                                         window_step_horizontal[i, 0]))
        n_windows_vertical = len(range(0, image_height[i, 0],
                                       window_step_vertical[i, 0]))
        assert_allclose(hog_im.shape, (n_windows_vertical,
                                       n_windows_horizontal))


def test_windowiterator_hog_no_padding():
    n_cases = 5
    image_width = np.random.randint(50, 250, [n_cases, 1])
    image_height = np.random.randint(50, 250, [n_cases, 1])
    window_step_horizontal = np.random.randint(1, 10, [n_cases, 1])
    window_step_vertical = np.random.randint(1, 10, [n_cases, 1])
    window_width = np.random.randint(3, 20, [n_cases, 1])
    window_height = np.random.randint(3, 20, [n_cases, 1])
    for i in range(n_cases):
        image = MaskedImage(np.random.randn(image_height[i, 0],
                                            image_width[i, 0], 1))
        hog_img = hog(image,
            mode='dense', cell_size=3, block_size=1,
            window_height=window_height[i, 0], window_width=window_width[i, 0],
            window_unit='pixels',
            window_step_vertical=window_step_vertical[i, 0],
            window_step_horizontal=window_step_horizontal[i, 0],
            window_step_unit='pixels', padding=False)
        n_windows_horizontal = len(range(window_width[i, 0] - 1,
                                         image_width[i, 0],
                                         window_step_horizontal[i, 0]))
        n_windows_vertical = len(range(window_height[i, 0] - 1,
                                       image_height[i, 0],
                                       window_step_vertical[i, 0]))
        assert_allclose(hog_img.shape, (n_windows_vertical,
                                        n_windows_horizontal))


def test_windowiterator_lbp_padding():
    n_cases = 5
    image_width = np.random.randint(50, 250, [n_cases, 1])
    image_height = np.random.randint(50, 250, [n_cases, 1])
    window_step_horizontal = np.random.randint(1, 10, [n_cases, 1])
    window_step_vertical = np.random.randint(1, 10, [n_cases, 1])
    for i in range(n_cases):
        image = MaskedImage(np.random.randn(image_height[i, 0],
                                            image_width[i, 0], 1))
        lbp_img = lbp(image,
            window_step_vertical=window_step_vertical[i, 0],
            window_step_horizontal=window_step_horizontal[i, 0],
            window_step_unit='pixels', padding=True)
        n_windows_horizontal = len(range(0, image_width[i, 0],
                                         window_step_horizontal[i, 0]))
        n_windows_vertical = len(range(0, image_height[i, 0],
                                       window_step_vertical[i, 0]))
        assert_allclose(lbp_img.shape, (n_windows_vertical,
                                          n_windows_horizontal))


def test_windowiterator_lbp_no_padding():
    n_cases = 5
    image_width = np.random.randint(50, 250, [n_cases, 1])
    image_height = np.random.randint(50, 250, [n_cases, 1])
    window_step_horizontal = np.random.randint(1, 10, [n_cases, 1])
    window_step_vertical = np.random.randint(1, 10, [n_cases, 1])
    radius = np.random.randint(3, 5, [n_cases, 1])
    for i in range(n_cases):
        image = Image(np.random.randn(image_height[i, 0],
                                      image_width[i, 0], 1))
        lbp_img = lbp(image,
            radius=radius[i, 0], samples=8,
            window_step_vertical=window_step_vertical[i, 0],
            window_step_horizontal=window_step_horizontal[i, 0],
            window_step_unit='pixels', padding=False)
        window_size = 2 * radius[i, 0] + 1
        n_windows_horizontal = len(range(window_size - 1, image_width[i, 0],
                                         window_step_horizontal[i, 0]))
        n_windows_vertical = len(range(window_size - 1, image_height[i, 0],
                                       window_step_vertical[i, 0]))
        assert_allclose(lbp_img.shape, (n_windows_vertical,
                                        n_windows_horizontal))


def test_hog_channels_dalaltriggs():
    n_cases = 3
    cell_size = np.random.randint(1, 10, [n_cases, 1])
    block_size = np.random.randint(1, 3, [n_cases, 1])
    num_bins = np.random.randint(7, 9, [n_cases, 1])
    channels = np.random.randint(1, 4, [n_cases, 1])
    for i in range(n_cases):
        image = MaskedImage(np.random.randn(40, 40, channels[i, 0]))
        block_size_pixels = cell_size[i, 0] * block_size[i, 0]
        window_width = np.random.randint(block_size_pixels, 40, 1)
        window_height = np.random.randint(block_size_pixels, 40, 1)
        hog_img = hog(image, mode='dense', algorithm='dalaltriggs',
                      cell_size=cell_size[i, 0], block_size=block_size[i, 0],
                      num_bins=num_bins[i, 0], window_height=window_height[0],
                      window_width=window_width[0], window_unit='pixels',
                      window_step_vertical=3, window_step_horizontal=3,
                      window_step_unit='pixels', padding=True)
        length_per_block = block_size[i, 0] * block_size[i, 0] * num_bins[i, 0]
        n_blocks_horizontal = len(range(block_size_pixels - 1, window_width[0],
                                        cell_size[i, 0]))
        n_blocks_vertical = len(range(block_size_pixels - 1, window_height[0],
                                      cell_size[i, 0]))
        n_channels = n_blocks_horizontal * n_blocks_vertical * length_per_block
        assert_allclose(hog_img.n_channels, n_channels)


def test_hog_channels_zhuramanan():
    n_cases = 3
    cell_size = np.random.randint(2, 10, [n_cases, 1])
    channels = np.random.randint(1, 4, [n_cases, 1])
    for i in range(n_cases):
        image = MaskedImage(np.random.randn(40, 40, channels[i, 0]))
        window_width = np.random.randint(3 * cell_size[i, 0], 40, 1)
        window_height = np.random.randint(3 * cell_size[i, 0], 40, 1)
        hog_img = hog(image, mode='dense', algorithm='zhuramanan',
                      cell_size=cell_size[i, 0],
                      window_height=window_height[0],
                      window_width=window_width[0],
                      window_unit='pixels', window_step_vertical=3,
                      window_step_horizontal=3,
                      window_step_unit='pixels', padding=True)
        length_per_block = 31
        n_blocks_horizontal = round(np.float(window_width[0])
                                       / np.float(cell_size[i, 0])) - 2
        n_blocks_vertical = round(np.float(window_height[0])
                                     / np.float(cell_size[i, 0])) - 2
        n_channels = n_blocks_horizontal * n_blocks_vertical * length_per_block
        assert_allclose(hog_img.n_channels, n_channels)


def test_lbp_channels():
    n_cases = 3
    n_combs = np.random.randint(1, 6, [n_cases, 1])
    channels = np.random.randint(1, 4, [n_cases, 1])
    for i in range(n_cases):
        radius = random.sample(xrange(1, 10), n_combs[i, 0])
        samples = random.sample(xrange(4, 12), n_combs[i, 0])
        image = MaskedImage(np.random.randn(40, 40, channels[i, 0]))
        lbp_img = lbp(image, radius=radius, samples=samples,
                      window_step_vertical=3, window_step_horizontal=3,
                      window_step_unit='pixels', padding=True)
        assert_allclose(lbp_img.n_channels, n_combs[i, 0] * channels[i, 0])


def test_igo_channels():
    n_cases = 3
    channels = np.random.randint(1, 10, [n_cases, 1])
    for i in range(n_cases):
        image = Image(np.random.randn(40, 40, channels[i, 0]))
        igo_img = igo(image)
        igo2_img = igo(image, double_angles=True)
        assert_allclose(igo_img.shape, image.shape)
        assert_allclose(igo2_img.shape, image.shape)
        assert_allclose(igo_img.n_channels, 2 * channels[i, 0])
        assert_allclose(igo2_img.n_channels, 4 * channels[i, 0])


def test_es_channels():
    n_cases = 3
    channels = np.random.randint(1, 10, [n_cases, 1])
    for i in range(n_cases):
        image = Image(np.random.randn(40, 40, channels[i, 0]))
        es_img = es(image)
        assert_allclose(es_img.shape, image.shape)
        assert_allclose(es_img.n_channels, 2 * channels[i, 0])


def test_igo_values():
    image = Image([[1, 2], [2, 1]])
    igo_img = igo(image)
    res = np.array([
        [[math.cos(math.radians(45)), math.sin(math.radians(45))],
         [math.cos(math.radians(90+45)), math.sin(math.radians(90+45))]],
        [[math.cos(math.radians(-45)), math.sin(math.radians(-45))],
         [math.cos(math.radians(180+45)), math.sin(math.radians(180+45))]]])
    assert_allclose(igo_img.pixels, res)
    image = Image([[0, 0], [0, 0]])
    igo_img = igo(image)
    res = np.array([[[1., 0.], [1., 0.]], [[1., 0.], [1., 0.]]])
    assert_allclose(igo_img.pixels, res)


def test_es_values():
    image = Image([[1, 2], [2, 1]])
    print image.shape
    es_img = es(image)
    k = 1 / (2 * (2**0.5))
    res = np.array([[[k, k], [-k, k]], [[k, -k], [-k, -k]]])
    assert_allclose(es_img.pixels, res)
    image = Image([[0, 0], [0, 0]])
    es_img = es(image)
    res = np.array([[[np.nan, np.nan], [np.nan, np.nan]],
                    [[np.nan, np.nan], [np.nan, np.nan]]])
    assert_allclose(es_img.pixels, res)


def test_lbp_values():
    image = Image([[0., 6., 0.], [5., 18., 13.], [0., 20., 0.]])
    lbp_img = lbp(image, radius=1, samples=4, mapping_type='none',
                  padding=False)
    assert_allclose(lbp_img.pixels, 8.)
    image = Image([[0., 6., 0.], [5., 25., 13.], [0., 20., 0.]])
    lbp_img = lbp(image, radius=1, samples=4, mapping_type='riu2',
                  padding=False)
    assert_allclose(lbp_img.pixels, 0.)
    image = Image([[0., 6., 0.], [5., 13., 13.], [0., 20., 0.]])
    lbp_img = lbp(image, radius=1, samples=4, mapping_type='u2', padding=False)
    assert_allclose(lbp_img.pixels, 8.)
    image = Image([[0., 6., 0.], [5., 6., 13.], [0., 20., 0.]])
    lbp_img = lbp(image, radius=1, samples=4, mapping_type='ri', padding=False)
    assert_allclose(lbp_img.pixels, 4.)


def test_constrain_landmarks():
    breaking_bad = mio.import_builtin_asset('breakingbad.jpg')
    breaking_bad.crop_to_landmarks_inplace(boundary=20)
    breaking_bad.constrain_mask_to_landmarks()
    breaking_bad = breaking_bad.resize([50, 50])
    hog_b = hog(breaking_bad, mode='sparse')
    x = np.where(hog_b.landmarks['PTS'].lms.points[:, 0] > hog_b.shape[1] - 1)
    y = np.where(hog_b.landmarks['PTS'].lms.points[:, 0] > hog_b.shape[0] - 1)
    assert_allclose(len(x[0]) + len(y[0]), 12)
    hog_b = hog(breaking_bad, mode='sparse')
    hog_b.constrain_landmarks_to_bounds()
    x = np.where(hog_b.landmarks['PTS'].lms.points[:, 0] > hog_b.shape[1] - 1)
    y = np.where(hog_b.landmarks['PTS'].lms.points[:, 0] > hog_b.shape[0] - 1)
    assert_allclose(len(x[0]) + len(y[0]), 0)
