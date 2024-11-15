from django.shortcuts import redirect
def para_onde_vou(request,link_antigo):
    link_lista = link_antigo.split("/")
    if "eletivas" in link_antigo:
        return redirect("/eletivas")
    elif "sobre" in link_antigo:
        return redirect("/sobre")
    elif "tutoria" in link_antigo:
        return redirect("/tutoria")
    elif "definir-paginas" in link_antigo:
        return redirect("/area-restrita/definir_paginas_utilizaveis")
    elif  link_antigo == "/":
        return redirect("/")
    if link_lista[2] == 'update_or_delete':
        print(f"/area-restrita/update_or_delete/{link_lista[3]}/{link_lista[4]}")
        return redirect(f"/area-restrita/update_or_delete/{link_lista[3]}/{link_lista[4]}")
    elif link_lista[2] == 'deletar' or link_lista[2] == 'atualizar':
        return redirect(f"/area-restrita/{link_lista[2]}/{link_lista[3]}/{link_lista[4]}")