import logging
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Citas disponibles y reservadas en memoria
citas_disponibles = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00"]
citas_reservadas = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hola {user.mention_html()}! Soy tu asistente para agendar citas en la barbería. Usa /ver_citas para ver las horas disponibles y /reservar <hora> para reservar una cita.",
        reply_markup=ForceReply(selective=True),
    )

async def ver_citas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with the available appointments."""
    if citas_disponibles:
        await update.message.reply_text(f"Citas disponibles: {', '.join(citas_disponibles)}")
    else:
        await update.message.reply_text("No hay citas disponibles.")

async def reservar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reserve an appointment."""
    if not context.args:
        await update.message.reply_text("Por favor, proporciona una hora para reservar. Ejemplo: /reservar 10:00")
        return

    hora = context.args[0]
    user_id = update.effective_user.id
    user_name = update.effective_user.full_name

    if hora in citas_disponibles:
        citas_disponibles.remove(hora)
        citas_reservadas[hora] = {"user_id": user_id, "user_name": user_name}
        await update.message.reply_text(f"Cita reservada a las {hora} para {user_name}.")
    else:
        await update.message.reply_text("La hora seleccionada no está disponible. Por favor, elige otra hora usando /ver_citas.")

def main() -> None:
    """Start the bot."""
    application = Application.builder().token("7317203420:AAEjKPjO7ajBs7NsqUQ0jM7UZWd5o-8kFRY").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ver_citas", ver_citas))
    application.add_handler(CommandHandler("reservar", reservar))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
