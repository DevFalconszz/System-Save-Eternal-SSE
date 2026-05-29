# 📱 SSE no Android

> Guia completo para usar o System Save Eternal em dispositivos Android

---

## Abordagens

Existem duas formas de usar o SSE no Android:

| Abordagem | Status | Descrição |
|-----------|--------|-----------|
| **Termux** | ✅ Funciona agora | Terminal Linux no Android, roda SSE via Python |
| **App Nativo** | 🔧 Proposto | Aplicativo Android nativo (Kotlin) — apenas documentado |

---

## 1️⃣ Termux (Recomendado)

### O que é Termux?

[Termux](https://termux.dev) é um emulador de terminal Linux para Android que permite rodar Python e outras ferramentas sem root.

### Instalação

```bash
# 1. Instale o Termux pela F-Droid (recomendado) ou Play Store
#    https://f-droid.org/packages/com.termux/

# 2. Atualize os pacotes
pkg update && pkg upgrade

# 3. Instale Python e Git
pkg install python git

# 4. Clone o SSE
git clone https://github.com/DevFalconszz/System-Save-Eternal-SSE.git
cd System-Save-Eternal-SSE

# 5. Instale as dependências
pip install -r requirements.txt

# 6. Execute
python src/main.py
```

### Compatibilidade com Emuladores Android

O SSE detecta automaticamente saves em diretórios do Termux no Android. Os seguintes emuladores têm saves detectáveis:

| Emulador | Caminho no Termux |
|----------|-------------------|
| **RetroArch** | `~/storage/shared/RetroArch/saves/` |
| **Drastic DS** | `~/storage/shared/draStic/backup/` |
| **Pizza Boy** | `~/storage/shared/com.pizzaboy/` |
| **MelonDS** | `~/storage/shared/melonDS/` |

> ℹ️ O SSE acessa os saves via `~/storage/shared/` (acesso ao armazenamento externo do Termux).

### Limitações no Android

| Funcionalidade | Suporte |
|----------------|---------|
| Backup de saves Minecraft | ❌ (Minecraft não está disponível no Android da mesma forma) |
| Backup de saves Pokémon (emuladores) | ✅ |
| Modo Jogar Minecraft | ❌ |
| GitHub | ✅ |
| Google Drive | ✅ (com `pydrive2`) |
| Telegram | ✅ (com `telethon`) |
| Interface gráfica (Tkinter) | ❌ (Termux não suporta Tkinter) |
| Modo CLI (terminal) | ✅ (fallback automático) |

### Dicas para Android

```bash
# Para acesso ao armazenamento externo
termux-setup-storage

# Para manter o SSE rodando mesmo com o app em segundo plano
# Vá em Configurações do Android → Apps → Termux → "Ignorar otimização de bateria"

# Para criar um atalho no launcher do Android:
# Use o app "Termux:Widget" para adicionar um atalho na tela inicial
```

---

## 2️⃣ App Nativo (Proposta)

> ⚠️ Esta seção documenta o **design proposto** para um futuro aplicativo Android nativo. Não há implementação disponível no momento.

### Arquitetura Proposta

```
┌──────────────────────────────────────────┐
│          SSE Android App                 │
│  ┌──────────────────────────────────┐   │
│  │         Interface (UI)           │   │
│  │  ┌─────────┐  ┌──────────────┐  │   │
│  │  │Material │  │  Terminal    │  │   │
│  │  │ Design  │  │  Log View    │  │   │
│  │  └────┬────┘  └──────┬───────┘  │   │
│  └───────┼──────────────┼──────────┘   │
│          ▼              ▼               │
│  ┌──────────────────────────────────┐   │
│  │        Core (Kotlin)             │   │
│  │  ┌──────────┐ ┌──────────────┐  │   │
│  │  │ Save     │ │ Backup       │  │   │
│  │  │ Scanner  │ │ Manager      │  │   │
│  │  └────┬─────┘ └──────┬───────┘  │   │
│  │       └──────┬───────┘          │   │
│  │              ▼                   │   │
│  │  ┌──────────────────────────┐   │   │
│  │  │  Storage Providers       │   │   │
│  │  │  (GitHub / Drive / TG)   │   │   │
│  │  └──────────────────────────┘   │   │
│  └──────────────────────────────────┘   │
│  ┌──────────────────────────────────┐   │
│  │     Android Permissions          │   │
│  │  • Storage (MANAGE_EXTERNAL)     │   │
│  │  • Internet                      │   │
│  │  • Notification (progresso)      │   │
│  └──────────────────────────────────┘   │
└──────────────────────────────────────────┘
```

### Funcionalidades Planejadas

| Funcionalidade | Status |
|----------------|--------|
| Scanner de saves (emuladores) | 📝 Planejado |
| Backup para GitHub | 📝 Planejado |
| Backup para Google Drive | 📝 Planejado |
| Backup para Telegram | 📝 Planejado |
| Agendamento automático | 📝 Planejado |
| Notificações de progresso | 📝 Planejado |
| Modo escuro | 📝 Planejado |
| Suporte a root (acesso total) | 🤔 Em estudo |

### Fluxo de Uso (App Nativo)

```
1. Abrir app → Tela de boas-vindas
2. Conceder permissões de armazenamento
3. App escaneia o dispositivo atrás de saves
   ├─ RetroArch:  /sdcard/RetroArch/saves/
   ├─ Drastic:    /sdcard/draStic/backup/
   ├─ Pizza Boy:  /sdcard/Android/data/com.pizzaboy/
   └─ Outros
4. Usuário seleciona quais saves incluir
5. Usuário configura destinos (GitHub, Drive, Telegram)
6. Backup é executado (com barra de progresso)
7. Opcional: agendar backups automáticos
```

### Tecnologias Sugeridas

| Tecnologia | Uso |
|------------|-----|
| **Kotlin** | Linguagem principal |
| **Jetpack Compose** | UI moderna |
| **Retrofit + OkHttp** | Comunicação com GitHub API |
| **Google Drive API (Android)** | Backup para Drive |
| **Telegram Bot API** | Backup para Telegram |
| **WorkManager** | Backup agendado em background |
| **Room** | Cache local de configurações |
| **DataStore** | Preferências do usuário |

### Exemplo de API (Kotlin)

```kotlin
// Interface hipotética para o Save Scanner
interface SaveScanner {
    suspend fun scan(): List<SaveEntry>
}

class RetroarchScanner(private val context: Context) : SaveScanner {
    override suspend fun scan(): List<SaveEntry> {
        val savesDir = File(
            Environment.getExternalStorageDirectory(),
            "RetroArch/saves"
        )
        return savesDir.listFiles()
            ?.filter { it.extension in listOf("sav", "state", "dsv") }
            ?.map { SaveEntry(
                name = it.name,
                path = it.absolutePath,
                game = detectGame(it.name),
                platform = "Android (RetroArch)",
                sizeBytes = it.length()
            ) } ?: emptyList()
    }
}
```

---

## 📋 Comparativo: Termux vs App Nativo

| Aspecto | Termux | App Nativo |
|---------|--------|------------|
| **Disponibilidade** | ✅ Hoje | ❌ Futuro |
| **Interface** | Terminal (CLI) | Material Design |
| **Notificações** | ❌ | ✅ |
| **Backup agendado** | ❌ (cron via Termux:Boot) | ✅ (WorkManager) |
| **Acesso a arquivos** | Via `termux-setup-storage` | API Storage Access Framework |
| **Tamanho** | ~100MB (Termux + Python) | ~15MB |
| **Configuração** | Manual (terminal) | Guiada (UI) |
| **Root necessário** | ❌ | ❌ (mas pode usar root extras) |

---

## 📱 Compatibilidade de Saves (Android)

### Emuladores Nintendo DS

| App | Detectável | Caminho típico |
|-----|-----------|----------------|
| Drastic DS | ✅ | `/sdcard/draStic/backup/` |
| RetroArch (cores DS) | ✅ | `/sdcard/RetroArch/saves/` |
| MelonDS Android | ✅ | `/sdcard/melonDS/` |
| Pizza Boy GBA | ✅ | `/sdcard/Android/data/com.pizzaboy/` |
| nds4droid | ✅ | `/sdcard/nds4droid/` |

### Emuladores GBA

| App | Detectável | Caminho típico |
|-----|-----------|----------------|
| My Boy! | ✅ | `/sdcard/MyBoy/saves/` |
| Pizza Boy GBA | ✅ | `/sdcard/Android/data/com.pizzaboy.gba/` |
| RetroArch (GBA cores) | ✅ | `/sdcard/RetroArch/saves/` |
| mGBA Android | ✅ | `/sdcard/mgba/` |

---

## 🔧 Setup Detalhado (Termux)

### Passo 1: Instalar Termux

```bash
# Baixe da F-Droid (recomendado)
# https://f-droid.org/packages/com.termux/
```

> ⚠️ A versão da Play Store pode estar desatualizada. Prefira F-Droid.

### Passo 2: Configurar armazenamento

```bash
# Concede acesso ao armazenamento externo
termux-setup-storage

# Verifique se o diretório foi criado
ls ~/storage/shared/
```

### Passo 3: Instalar dependências

```bash
pkg update && pkg upgrade -y
pkg install python git openssh -y
```

### Passo 4: Clonar e executar

```bash
git clone https://github.com/DevFalconszz/System-Save-Eternal-SSE.git
cd System-Save-Eternal-SSE
pip install -r requirements.txt
python src/main.py
```

> ℹ️ No Termux, o Tkinter não está disponível, então o SSE usará automaticamente o modo CLI.

### Passo 5 (opcional): Atalho via script

```bash
# Crie um script executável
echo '#!/data/data/com.termux/files/usr/bin/bash
cd ~/System-Save-Eternal-SSE
python src/main.py "$@"' > $PREFIX/bin/sse
chmod +x $PREFIX/bin/sse

# Agora é só digitar "sse" no terminal
sse
```

### Backup Agendado (Termux)

```bash
# Instale Termux:Cron e Termux:Boot
pkg install cronie termux-services

# Adicione ao crontab
crontab -e

# Exemplo: backup automático todos os dias às 22:00
0 22 * * * cd ~/System-Save-Eternal-SSE && python src/main.py --auto-backup

# Ative o serviço de cron
sv-enable crond
```

---

> Para mais informações sobre o SSE, consulte o [`README.md`](../README.md) principal.
