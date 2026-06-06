// Simple example to verify PDFium library linking and basic functionality.
// Loads a PDF document from file and prints page count.

#include <cstring>
#include <iostream>
#include <string>
#include <vector>

#include "fpdfview.h"

// Simple file read helper
std::vector<uint8_t> ReadFile(const std::string& path) {
  FILE* fp = fopen(path.c_str(), "rb");
  if (!fp) return {};

  fseek(fp, 0, SEEK_END);
  long size = ftell(fp);
  fseek(fp, 0, SEEK_SET);

  std::vector<uint8_t> buf(size);
  fread(buf.data(), 1, size, fp);
  fclose(fp);
  return buf;
}

int main(int argc, char* argv[]) {
  // Initialize PDFium library
  FPDF_InitLibrary();
  std::cout << "PDFium library initialized successfully!" << std::endl;

  if (argc < 2) {
    std::cout << "Usage: hello_pdfium <pdf_file>" << std::endl;
    std::cout << "Skipping document loading (no file specified)." << std::endl;
    FPDF_DestroyLibrary();
    return 0;
  }

  const char* filename = argv[1];
  auto file_data = ReadFile(filename);

  if (file_data.empty()) {
    std::cerr << "Error: Could not open file: " << filename << std::endl;
    FPDF_DestroyLibrary();
    return 1;
  }

  // Load document from memory
  FPDF_DOCUMENT doc = FPDF_LoadMemDocument(file_data.data(), file_data.size(), nullptr);

  if (!doc) {
    unsigned long err = FPDF_GetLastError();
    std::cerr << "Error loading PDF (error code: " << err << "): ";
    switch (err) {
      case FPDF_ERR_SUCCESS:
        std::cerr << "Success";
        break;
      case FPDF_ERR_UNKNOWN:
        std::cerr << "Unknown error";
        break;
      case FPDF_ERR_FILE:
        std::cerr << "File not found or cannot be opened";
        break;
      case FPDF_ERR_FORMAT:
        std::cerr << "File not in PDF format or corrupted";
        break;
      case FPDF_ERR_PASSWORD:
        std::cerr << "Password required or incorrect password";
        break;
      case FPDF_ERR_SECURITY:
        std::cerr << "Unsupported security scheme";
        break;
      case FPDF_ERR_PAGE:
        std::cerr << "Page not found or content error";
        break;
      default:
        std::cerr << "Unknown error code";
        break;
    }
    std::cerr << std::endl;
    FPDF_DestroyLibrary();
    return 1;
  }

  int page_count = FPDF_GetPageCount(doc);
  std::cout << "PDF loaded successfully!" << std::endl;
  std::cout << "File: " << filename << std::endl;
  std::cout << "Page count: " << page_count << std::endl;

  FPDF_CloseDocument(doc);
  FPDF_DestroyLibrary();

  std::cout << "PDFium test completed successfully!" << std::endl;
  return 0;
}
