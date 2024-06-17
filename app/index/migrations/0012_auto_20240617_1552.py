# Generated by Django 3.2.25 on 2024-06-17 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0011_chat_mensagem_produtoalugado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anuncio',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='anuncio',
            name='descricao',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='anuncio',
            name='estado',
            field=models.CharField(choices=[('Novo', 'Novo'), ('Semi-novo', 'Semi-novo'), ('Usado', 'Usado')], default='Novo', max_length=10),
        ),
        migrations.AlterField(
            model_name='anuncio',
            name='titulo',
            field=models.CharField(default='Título do Anúncio', max_length=255),
        ),
        migrations.AlterField(
            model_name='anuncio',
            name='utilizador',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='index.utilizador'),
        ),
    ]
