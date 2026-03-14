"""
Image compression and resize helpers for uploaded admin images.

The utility prefers Pillow for reliable local resizing. TinyPNG support is
optional and only used when explicitly enabled and the dependency is installed.
"""

import os
from io import BytesIO

try:
    import tinify
except ImportError:  # pragma: no cover - optional dependency
    tinify = None

try:
    from PIL import Image, ImageOps, UnidentifiedImageError
except ImportError:  # pragma: no cover - Pillow is expected in production
    Image = None
    ImageOps = None
    UnidentifiedImageError = Exception


TINYPNG_API_KEYS = [key.strip() for key in os.environ.get('TINYPNG_API_KEYS', '').split(',') if key.strip()]
DEFAULT_MAX_WIDTH = 0
DEFAULT_MAX_HEIGHT = 0
DEFAULT_JPEG_QUALITY = 80


def _build_result(success, message, original_size=0, compressed_size=0, output_path=''):
    saved_percent = 0
    if success and original_size and compressed_size:
        saved_percent = round((1 - compressed_size / original_size) * 100, 2)

    return {
        'success': success,
        'message': message,
        'original_size': original_size,
        'compressed_size': compressed_size,
        'saved_percent': saved_percent,
        'output_path': output_path,
    }


def _compress_with_tinypng(input_path, temp_path, api_keys=None):
    keys = api_keys if api_keys is not None else TINYPNG_API_KEYS
    if tinify is None or not keys:
        return False, 'TinyPNG is not configured'

    for key in keys:
        try:
            tinify.key = key
            source = tinify.from_file(input_path)
            source.to_file(temp_path)
            return True, None
        except tinify.AccountError:
            continue
        except tinify.ClientError as exc:
            return False, f'Invalid image for TinyPNG: {exc}'
        except Exception as exc:  # pragma: no cover - network/service specific
            return False, f'TinyPNG failed: {exc}'

    return False, 'No working TinyPNG API key available'


def _thumbnail_image(img, max_width, max_height):
    if not max_width and not max_height:
        return img

    width_limit = max_width or img.width
    height_limit = max_height or img.height
    if img.width <= width_limit and img.height <= height_limit:
        return img

    resampling = getattr(getattr(Image, 'Resampling', Image), 'LANCZOS')
    img.thumbnail((width_limit, height_limit), resampling)
    return img


def _save_with_pillow(source_path, output_path, jpeg_quality, max_width, max_height):
    if Image is None:
        return False, 'Pillow is not installed'

    try:
        with Image.open(source_path) as img:
            if ImageOps is not None:
                img = ImageOps.exif_transpose(img)

            img = _thumbnail_image(img, max_width, max_height)
            extension = os.path.splitext(output_path)[1].lower()
            save_kwargs = {'optimize': True}
            image_to_save = img

            if extension in {'.jpg', '.jpeg'}:
                save_format = 'JPEG'
                image_to_save = img.convert('RGB')
                save_kwargs.update({'quality': jpeg_quality, 'progressive': True})
            elif extension == '.png':
                save_format = 'PNG'
                if img.mode not in ('RGB', 'RGBA', 'L', 'LA', 'P'):
                    image_to_save = img.convert('RGBA')
            elif extension == '.webp':
                save_format = 'WEBP'
                save_kwargs.update({'quality': jpeg_quality})
            else:
                save_format = img.format or 'PNG'

            image_to_save.save(output_path, format=save_format, **save_kwargs)
            return True, None
    except UnidentifiedImageError:
        return False, 'Uploaded file is not a supported image'
    except OSError as exc:
        return False, f'Image save failed: {exc}'


def compress_image(
    input_path,
    output_path=None,
    jpeg_quality=DEFAULT_JPEG_QUALITY,
    max_width=DEFAULT_MAX_WIDTH,
    max_height=DEFAULT_MAX_HEIGHT,
    use_tinypng=False,
    api_keys=None,
):
    if not os.path.exists(input_path):
        return _build_result(False, f'File not found: {input_path}')

    output_path = output_path or input_path
    original_size = os.path.getsize(input_path)
    tinypng_temp_path = f'{input_path}.tinypng'
    optimized_temp_path = f'{output_path}.optimized'
    source_path = input_path

    try:
        if use_tinypng:
            success, error_message = _compress_with_tinypng(input_path, tinypng_temp_path, api_keys=api_keys)
            if success:
                source_path = tinypng_temp_path
            elif Image is None:
                return _build_result(False, error_message, original_size=original_size)

        success, error_message = _save_with_pillow(
            source_path,
            optimized_temp_path,
            jpeg_quality=jpeg_quality,
            max_width=max_width,
            max_height=max_height,
        )
        if not success:
            return _build_result(False, error_message, original_size=original_size)

        os.replace(optimized_temp_path, output_path)
        compressed_size = os.path.getsize(output_path)
        return _build_result(
            True,
            'Image resized and optimized successfully',
            original_size=original_size,
            compressed_size=compressed_size,
            output_path=output_path,
        )
    finally:
        for temp_path in (tinypng_temp_path, optimized_temp_path):
            if os.path.exists(temp_path):
                os.remove(temp_path)


def compress_uploaded_image(
    image_field,
    jpeg_quality=DEFAULT_JPEG_QUALITY,
    max_width=DEFAULT_MAX_WIDTH,
    max_height=DEFAULT_MAX_HEIGHT,
    use_tinypng=False,
    api_keys=None,
):
    if not image_field:
        return _build_result(False, 'Image field is empty')

    try:
        image_path = image_field.path
    except (ValueError, NotImplementedError):
        return _build_result(False, 'Image field does not have a local file path')

    return compress_image(
        input_path=image_path,
        jpeg_quality=jpeg_quality,
        max_width=max_width,
        max_height=max_height,
        use_tinypng=use_tinypng,
        api_keys=api_keys,
    )


def compress_in_memory(
    image_data,
    filename,
    jpeg_quality=DEFAULT_JPEG_QUALITY,
    max_width=DEFAULT_MAX_WIDTH,
    max_height=DEFAULT_MAX_HEIGHT,
):
    if Image is None:
        return {
            'success': False,
            'message': 'Pillow is not installed',
        }

    original_size = len(image_data)
    extension = os.path.splitext(filename)[1].lower()

    try:
        with Image.open(BytesIO(image_data)) as img:
            if ImageOps is not None:
                img = ImageOps.exif_transpose(img)
            img = _thumbnail_image(img, max_width, max_height)
            output = BytesIO()

            save_kwargs = {'optimize': True}
            image_to_save = img
            if extension in {'.jpg', '.jpeg'}:
                image_to_save = img.convert('RGB')
                image_to_save.save(output, format='JPEG', quality=jpeg_quality, progressive=True, **save_kwargs)
            elif extension == '.png':
                if img.mode not in ('RGB', 'RGBA', 'L', 'LA', 'P'):
                    image_to_save = img.convert('RGBA')
                image_to_save.save(output, format='PNG', **save_kwargs)
            elif extension == '.webp':
                image_to_save.save(output, format='WEBP', quality=jpeg_quality, **save_kwargs)
            else:
                image_to_save.save(output, format=img.format or 'PNG', **save_kwargs)

        compressed_data = output.getvalue()
        return {
            'success': True,
            'data': compressed_data,
            'original_size': original_size,
            'compressed_size': len(compressed_data),
            'saved_percent': round((1 - len(compressed_data) / original_size) * 100, 2) if original_size else 0,
            'message': 'Image resized and optimized successfully',
        }
    except UnidentifiedImageError:
        return {
            'success': False,
            'message': 'Uploaded bytes are not a supported image',
        }


def setup_auto_compress(model_class, image_field_name):
    from django.db.models.signals import post_save
    from django.dispatch import receiver

    @receiver(post_save, sender=model_class)
    def auto_compress_image(sender, instance, created, **kwargs):
        image_field = getattr(instance, image_field_name, None)
        if image_field:
            compress_uploaded_image(image_field)

    return auto_compress_image
