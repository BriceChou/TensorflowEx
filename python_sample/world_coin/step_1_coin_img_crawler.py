#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from requests_html import HTMLSession
from logger import Logger
import warnings
import traceback

warnings.filterwarnings('ignore')
session = HTMLSession()

with open('debug.log', 'w') as sf:
    sf.write('-*-*========== All start to Running ... ==========*-*-\n')

# create log file in current folder
log = Logger('debug.log', level='debug')


def download(url, filepath, backup_url=None):
    if os.path.exists(filepath):
        log.logger.error('This file {} aready existed.'.format(filepath))
        return
    try:
        r = session.get(url, stream=True, timeout=60)
        log.logger.debug('Website URL status code is {}'.format(r.status_code))
        if 200 == r.status_code:
            log.logger.debug('Start to save file {}'.format(filepath))
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    # filter out keep-alive new chunks
                    if chunk:
                        f.write(chunk)
                        f.flush()
            log.logger.debug('{} saved.'.format(filepath))
            return filepath
        else:
            download(backup_url, filepath)
            return filepath
    except KeyboardInterrupt:
        if os.path.exists(filepath):
            os.remove(filepath)
        raise KeyboardInterrupt
    except Exception:
        traceback.print_exc()
        if os.path.exists(filepath):
            os.remove(filepath)


def download_single_country_coin_img(
    base_url, backup_url, country_link_name, img_folder_path
):
    small_img_base_url = '{}countries/'.format(base_url)
    big_img_base_url = '{}wcg/img_hr/'.format(backup_url)
    country_link = '{}_all'.format(country_link_name)
    url = '{}{}.php'.format(small_img_base_url, country_link)

    try:
        log.logger.debug('Start to load website {}'.format(url))
        r = session.get(url, stream=True, timeout=60)
        if 200 == r.status_code:
            img_list = r.html.find('td > img')
            text_list = r.html.find('img + br')
            log.logger.info('image list size is {}'.format(len(img_list)))
            for (img, text) in zip(img_list, text_list):
                src_url = img.attrs.get('src')
                img_url = big_img_base_url + src_url
                backup_img_url = small_img_base_url + src_url
                img_name = (
                    text.text.replace(',', '')
                    .replace('.', '')
                    .replace('/', 'divided_by')
                    .replace(' ', '_')
                )
                img_type = img.attrs.get('src').split('.')[-1]
                img_path = '{}/{}.{}'.format(img_folder_path, img_name, img_type)
                log.logger.debug('Start to download image URL: {}'.format(img_url))
                download(img_url, img_path, backup_img_url)
        else:
            log.logger.error('Failed to open URL: {}.\n'.format(url))
    except KeyError:
        raise ValueError(f'Oops! There is no any images and text.')


base_url = 'http://worldcoingallery.com/'
backup_base_url = 'http://worldbanknotegallery.com/'
country_list_url = '{}index-EN.htm'.format(base_url)
main_folder_name = 'imgs'

# Create the image floder to save the image
if os.path.exists(main_folder_name) is False:
    os.makedirs(main_folder_name)

try:
    r = session.get(country_list_url, stream=True, timeout=60)
    if 200 == r.status_code:
        country_link_list = r.html.find('b > a')
        log.logger.info('country link list size is {}'.format(len(country_link_list)))
        for item in country_link_list:
            country_link_name = item.attrs.get('href').replace('/', '.').split('.')[-2]
            img_folder_path = os.path.join(main_folder_name, country_link_name)
            if os.path.exists(img_folder_path) is False:
                os.makedirs(img_folder_path)
            download_single_country_coin_img(
                base_url, backup_base_url, country_link_name, img_folder_path
            )
    else:
        log.logger.error('Failed to open URL: {}'.format(country_list_url))
except KeyError:
    raise ValueError(f'Oops! There is no any country.')
