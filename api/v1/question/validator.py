from django.core.validators import FileExtensionValidator

question_file_validation = [FileExtensionValidator(allowed_extensions=['mp3', 'jpg', 'jpeg', 'img', 'png'])]