# 📡 Download de Imagens Sentinel-2 com Google Earth Engine

Este projeto permite baixar imagens Sentinel-2 de alta resolução utilizando a API do Google Earth Engine. Ele processa uma geometria (WKT) para delimitar a área de interesse, aplica uma visualização RGB personalizada com ajuste de gama e exporta automaticamente a imagem para o Google Drive. Após a exportação, a imagem pode ser baixada e visualizada no QGIS.

## 🚀 Funcionalidades

- Autenticação e inicialização da API Earth Engine
- Seleção da melhor imagem Sentinel-2 (menos cobertura de nuvem nos últimos 30 dias)
- Aplicação de visualização RGB com gama personalizada
- Exportação automática para o Google Drive com buffer
- Download automático do arquivo do Drive para pasta local

## 🛠️ Requisitos

- Python 3.10+
- Conta Google com acesso ao Google Earth Engine e Google Drive


## 🔑 Autenticação
Você deve estar autenticado no Google Earth Engine e Google Drive para executar o script corretamente.