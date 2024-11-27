-- CreateTable
CREATE TABLE "Tratamento" (
    "id" SERIAL NOT NULL,
    "data_inicio" TIMESTAMP(3) NOT NULL,
    "data_finalizacao" TIMESTAMP(3),
    "medicamento_id" INTEGER NOT NULL,
    "user_id" TEXT NOT NULL,
    "lembrete_tomar_remedio" TIMESTAMP(3),
    "lembrete_remedio_acabando" TIMESTAMP(3),

    CONSTRAINT "Tratamento_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "Tratamento" ADD CONSTRAINT "Tratamento_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Tratamento" ADD CONSTRAINT "Tratamento_medicamento_id_fkey" FOREIGN KEY ("medicamento_id") REFERENCES "Medicamento"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
