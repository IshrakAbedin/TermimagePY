// Core.cpp : Defines the exported functions for the DLL application.

// Last modified by: Mohammad Ishrak Abedin, 24-11-2020

#include "stdafx.h"

#define ESC "\x1b"
#define CSI "\x1b["

void ccont_Init();
void ccont_EnableVT();
void ccont_DisableVT();
bool ccont_IsVTAlreadyOn();

DWORD ccont_default_in_mode;
DWORD ccont_default_out_mode;
HANDLE ccont_hStdin;
HANDLE ccont_hStdout;
bool cc_init = false;

constexpr char block = 219;

extern "C"
{
	_declspec(dllexport) void _stdcall printcolor(unsigned char* r, unsigned char* g, unsigned char* b, unsigned int rowCount, unsigned int colCount)
	{
		ccont_Init();
		bool isTermOnByDef = ccont_IsVTAlreadyOn();
		if (!isTermOnByDef) ccont_EnableVT();

		for (auto rc = 0; rc < rowCount; rc++)
		{
			for (auto cc = 0; cc < colCount; cc++)
			{
				printf(ESC "[38;2;%d;%d;%dm%c", r[rc * colCount + cc], g[rc * colCount + cc], b[rc * colCount + cc], block);
			}
			printf("\n");
		}
		printf(ESC "[0m");
		if (!isTermOnByDef) ccont_DisableVT();
	}
}

// Initialize Console Controller
void ccont_Init()
{
	ccont_hStdin = GetStdHandle(STD_INPUT_HANDLE);
	ccont_hStdout = GetStdHandle(STD_OUTPUT_HANDLE);
	GetConsoleMode(ccont_hStdin, &ccont_default_in_mode);
	GetConsoleMode(ccont_hStdout, &ccont_default_out_mode);
	cc_init = true;
}

// Enable virtual terminal emulation
void ccont_EnableVT()
{
	if (cc_init) SetConsoleMode(ccont_hStdout, ccont_default_out_mode | ENABLE_VIRTUAL_TERMINAL_PROCESSING);
	else printf("Initialize Console Controller First\n");
}

// Restore terminal to the default state as encountered first
void ccont_DisableVT()
{
	if (cc_init) SetConsoleMode(ccont_hStdout, ccont_default_out_mode);
	else printf("Initialize Console Controller First\n");
}

// Check whether virtual terminal emulation is on by default
bool ccont_IsVTAlreadyOn()
{
	if (cc_init) return ccont_default_out_mode == (ccont_default_out_mode | ENABLE_VIRTUAL_TERMINAL_PROCESSING);
	else printf("Initialize Console Controller First\n");
}