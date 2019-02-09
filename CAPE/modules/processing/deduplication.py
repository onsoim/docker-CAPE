# Copyright (C) 2017 Marirs.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import os
import logging
import imagehash
from PIL import Image
import six

from lib.cuckoo.common.abstracts import Processing
log = logging.getLogger()

class Deduplicate(Processing):
    """Deduplicate screenshots."""

    def deduplicate_images(self, userpath, hashfunc=imagehash.average_hash):
        """
        Remove duplicate images from a path
        :userpath: path of the image files
        :hashfunc: type of image hashing method
        """

        def is_image(filename):
            img_ext = [".jpg", ".png", ".gif", ".bmp", ".gif"]
            f = filename.lower()
            return any(f.endswith(ext) for ext in img_ext)

        """
        Available hashs functions:
            ahash:      Average hash
            phash:      Perceptual hash
            dhash:      Difference hash
            whash-haar: Haar wavelet hash
            whash-db4:  Daubechies wavelet hash
        """
        dd_img_set = []

        image_filenames = [os.path.join(userpath, path) for path in os.listdir(userpath) if is_image(path)]
        images = {}
        for img in sorted(image_filenames):
            hash = hashfunc(Image.open(img))
            images[hash] = images.get(hash, []) + [img]
        for k, img_list in six.iteritems(images):
            dd_img_set.append(os.path.basename(img_list[0]))
        dd_img_set.sort()
        return dd_img_set

    def run(self):
        """Creates a new key in the report dict for 
        the deuplicated screenshots.
        """
        self.key = "deduplicated_shots"
        shots = []

        try:
            hashmethod = "whash-db4"
            if hashmethod == 'ahash':
                hashfunc = imagehash.average_hash
            elif hashmethod == 'phash':
                hashfunc = imagehash.phash
            elif hashmethod == 'dhash':
                hashfunc = imagehash.dhash
            elif hashmethod == 'whash-haar':
                hashfunc = imagehash.whash
            elif hashmethod == 'whash-db4':
                hashfunc = lambda img: imagehash.whash(img, mode='db4')

            shots_path = os.path.join(self.analysis_path, "shots")
            if os.path.exists(shots_path):
                screenshots = self.deduplicate_images(userpath=shots_path, hashfunc=hashfunc)
                for screenshot in screenshots:
                    shots.append(screenshot.replace(".jpg",""))
        except Exception as e:
            log.error(e)

        return shots
