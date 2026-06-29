# Setup Google Calendar

1. Crie um projeto no Google Cloud.
2. Habilite Google Calendar API.
3. Crie OAuth Client.
4. Gere refresh token com escopo de calendario.
5. Configure `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`.
6. Defina `GOOGLE_CALENDAR_ID` ou salve calendario por corretor em `brokers.google_calendar_id`.

O workflow de calendario recebe cliente, imovel, corretor e janela desejada. Ele consulta disponibilidade, sugere dois horarios e cria evento quando o cliente escolhe.
