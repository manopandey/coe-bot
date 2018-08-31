module.exports = {
  apps : [{
    name   : "CoeBot",
    script : "./coeBot.py",
    watch  : true,
    interpreter  : "python3",
    env: {
      "TELEGRAM_TOKEN": "551736443:AAFrYyt2GRNov7n1A6RPojE-9jk-NQSEaIg",
      "NODE_ENV": "production"
    }
  }]
}
