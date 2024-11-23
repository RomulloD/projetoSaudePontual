-- CreateTable
CREATE TABLE "User" (
    "id" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "age" INTEGER NOT NULL DEFAULT 18,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "User_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Medicamento" (
    "id" SERIAL NOT NULL,
    "tipo_produto" TEXT NOT NULL,
    "nome_produto" TEXT NOT NULL,
    "data_finalizacao_processo" TIMESTAMP(3),
    "categoria_regulatoria" TEXT NOT NULL,
    "numero_registro_produto" TEXT NOT NULL,
    "data_vencimento_registro" TIMESTAMP(3),
    "numero_processo" TEXT NOT NULL,
    "classe_terapeutica" TEXT NOT NULL,
    "empresa_detentora_registro" TEXT NOT NULL,
    "situacao_registro" TEXT NOT NULL,
    "principio_ativo" TEXT,

    CONSTRAINT "Medicamento_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "User_email_key" ON "User"("email");

-- CreateIndex
CREATE UNIQUE INDEX "Medicamento_numero_registro_produto_key" ON "Medicamento"("numero_registro_produto");
