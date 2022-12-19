def insert(table, args, data, mysql):
    # create cursor obj
    cursor = mysql.connection.cursor()

    # build the sql string statement
    sql_args = ""
    values = ""

    for arg in args:
        sql_args += f"`{arg}`, "
        values += f"%s, "
    
    sql_args = sql_args[:-2]
    values = values[:-2]

    sql = f"""INSERT INTO `{table}` ({sql_args}) VALUES ({values})"""
    
    # sending data to the databse
    try:
        cursor.execute(sql, data)
        mysql.connection.commit()
    except:
        mysql.connection.rollback()
    
    cursor.close()