#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Donny You(youansheng@gmail.com)


from torch.utils import data

from datasets.test.loader.default_loader import DefaultLoader
from datasets.tools.collate import collate
from datasets.tools.transforms import ToTensor, Normalize, Compose
import datasets.tools.pil_aug_transforms as pil_aug_trans
import datasets.tools.cv2_aug_transforms as cv2_aug_trans
from utils.tools.logger import Logger as Log


class TestDataLoader(object):

    def __init__(self, configer):
        self.configer = configer

        if self.configer.get('data', 'image_tool') == 'pil':
            self.aug_test_transform = pil_aug_trans.PILAugCompose(self.configer, split='test')
        elif self.configer.get('data', 'image_tool') == 'cv2':
            self.aug_test_transform = cv2_aug_trans.CV2AugCompose(self.configer, split='test')
        else:
            Log.error('Not support {} image tool.'.format(self.configer.get('data', 'image_tool')))
            exit(1)

        self.img_transform = Compose([
            ToTensor(),
            Normalize(**self.configer.get('data', 'normalize')), ])

    def get_testloader(self, test_dir=None, list_path=None):
        test_dir = test_dir if test_dir is not None else self.configer.get('test', 'data_dir')
        if not self.configer.exists('test', 'loader') or self.configer.get('test', 'loader') == 'default':
            trainloader = data.DataLoader(
                DefaultLoader(test_dir=test_dir,
                              list_path=list_path,
                              aug_transform=self.aug_test_transform,
                              img_transform=self.img_transform,
                              configer=self.configer),
                batch_size=self.configer.get('test', 'batch_size'), shuffle=False,
                num_workers=self.configer.get('data', 'workers'), pin_memory=True,
                collate_fn=lambda *args: collate(
                    *args, trans_dict=self.configer.get('test', 'data_transformer')
                )
            )

            return trainloader

        else:
            Log.error('{} train loader is invalid.'.format(self.configer.get('train', 'loader')))
            exit(1)

